class ReportAgent:
    def __init__(self):
        pass

    def run(self, analysis: dict):
        report = f"""
        # Financial Analysis Report

        **Rating:** {analysis.get('rating')}
        **Rationale:** {analysis.get('rationale')}
        **Risk Level:** {analysis.get('risk_level')}
        **Time Horizon:** {analysis.get('time_horizon')}
        """
        return report
