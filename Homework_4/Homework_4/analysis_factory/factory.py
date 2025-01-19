from analysis_factory.technical_analysis import TechnicalAnalysis
from analysis_factory.fundamental_analysis import FundamentalAnalysis
from analysis_factory.lstm_analysis import LSTMAnalysis


class AnalysisFactory:
    @staticmethod
    def create_analysis(analysis_type, data):
        if analysis_type == "technical":
            return TechnicalAnalysis(data)
        elif analysis_type == "fundamental":
            return FundamentalAnalysis(data)
        elif analysis_type == "lstm":
            return LSTMAnalysis(data)
        else:
            raise ValueError(f"Unsupported analysis type: {analysis_type}")
