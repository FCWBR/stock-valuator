import math

class StockValuator:
    def __init__(self, ticker, price, eps_ttm, eps_fwd, bvps, dividend, 
                 g_div, fcf, g_fcf, g_terminal, discount_rate, pe_target, sector):
        self.ticker = ticker
        self.price = price
        self.eps_ttm = eps_ttm
        self.eps_fwd = eps_fwd
        self.bvps = bvps
        self.dividend = dividend
        self.g_div = g_div
        self.fcf = fcf
        self.g_fcf = g_fcf
        self.g_terminal = g_terminal
        self.r = discount_rate
        self.pe_target = pe_target
        self.sector = sector.lower()

    def calc_dcf(self, years=5):
        """Calculates Discounted Cash Flow (5-year projection + Terminal Value)"""
        dcf_value = 0
        current_fcf = self.fcf
        
        # Calculate Present Value of 5-year FCF
        for t in range(1, years + 1):
            projected_fcf = current_fcf * ((1 + self.g_fcf) ** t)
            dcf_value += projected_fcf / ((1 + self.r) ** t)
            
        # Calculate Terminal Value and discount to present
        terminal_fcf = current_fcf * ((1 + self.g_fcf) ** years)
        terminal_value = (terminal_fcf * (1 + self.g_terminal)) / (self.r - self.g_terminal)
        pv_terminal_value = terminal_value / ((1 + self.r) ** years)
        
        return dcf_value + pv_terminal_value

    def calc_ddm(self):
        """Calculates Dividend Discount Model (Gordon Growth Model)"""
        if self.dividend <= 0:
            return 0
        # Rule D: Prevent broken yield math if growth exceeds discount rate
        safe_g_div = min(self.g_div, self.r - 0.01)
        return (self.dividend * (1 + safe_g_div)) / (self.r - safe_g_div)

    def calc_pe_multiple(self):
        """Calculates Relative Valuation based on Forward P/E"""
        if self.eps_fwd <= 0:
            return 0
        return (self.eps_fwd * self.pe_target) / (1 + self.r)

    def calc_graham_number(self):
        """Calculates Benjamin Graham's defensive value"""
        if self.eps_ttm <= 0 or self.bvps <= 0:
            return 0
        return math.sqrt(22.5 * self.eps_ttm * self.bvps)

    def evaluate(self):
        """Runs the conditional logic and calculates blended intrinsic value"""
        # Step 1: Calculate raw model values
        v_dcf = self.calc_dcf()
        v_ddm = self.calc_ddm()
        v_pe = self.calc_pe_multiple()
        v_graham = self.calc_graham_number()

        # Step 2: Initialize default weights
        weights = {"DCF": 0.25, "DDM": 0.25, "PE": 0.25, "Graham": 0.25}

        # Step 3: Apply Conditional Logic (Rules A, B, C)
        # Rule A: Non-Dividend Payers
        if self.dividend <= 0:
            weights["DDM"] = 0
            
        # Rule B: Asset-Light / Service Sectors / Negative BVPS
        service_sectors = ["technology", "healthcare", "services", "software"]
        if self.bvps <= 0 or self.sector in service_sectors:
            weights["Graham"] = 0
            
        # Rule C: Negative Earnings
        if self.eps_ttm <= 0:
            weights["Graham"] = 0
            weights["PE"] = 0

        # Step 4: Normalize weights so they add up to 1.0 (100%)
        active_weight_count = sum(1 for w in weights.values() if w > 0)
        if active_weight_count == 0:
            return "Error: No valid valuation models available for this data."
        
        adjusted_weight = 1.0 / active_weight_count
        for key in weights:
            if weights[key] > 0:
                weights[key] = adjusted_weight

        # Step 5: Calculate Blended Value
        blended_value = (v_dcf * weights["DCF"]) + \
                        (v_ddm * weights["DDM"]) + \
                        (v_pe * weights["PE"]) + \
                        (v_graham * weights["Graham"])

        # Step 6: Generate Verdict
        verdict = "UNDERVALUED" if self.price < blended_value else "OVERVALUED"
        discount = ((blended_value - self.price) / blended_value) * 100

        # Print Output
        print(f"--- {self.ticker} VALUATION REPORT ---")
        print(f"Current Price:  ${self.price:.2f}")
        print("-" * 30)
        print(f"DCF Value:      ${v_dcf:.2f} (Weight: {weights['DCF']*100:.1f}%)")
        print(f"DDM Value:      ${v_ddm:.2f} (Weight: {weights['DDM']*100:.1f}%)")
        print(f"P/E Value:      ${v_pe:.2f} (Weight: {weights['PE']*100:.1f}%)")
        print(f"Graham Value:   ${v_graham:.2f} (Weight: {weights['Graham']*100:.1f}%)")
        print("-" * 30)
        print(f"Blended Value:  ${blended_value:.2f}")
        print(f"Verdict:        {verdict} (Diff: {discount:.2f}%)")


# --- RUNNING THE UNH SCENARIO ---
if __name__ == "__main__":
    # Initializing UNH with the 2026 data we discussed
    unh = StockValuator(
        ticker="UNH",
        price=269.35,
        eps_ttm=13.23,
        eps_fwd=17.75,
        bvps=106.00,
        dividend=8.84,
        g_div=0.06,
        fcf=16.00,
        g_fcf=0.06,
        g_terminal=0.025,
        discount_rate=0.09,
        pe_target=17.0,
        sector="Healthcare" # This will trigger Rule B and zero out the Graham Number
    )
    
    unh.evaluate()
