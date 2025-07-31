# 🌱 Crypto ESG Dashboard

A real-time cryptocurrency dashboard that combines live price data with Environmental, Social, and Governance (ESG) scores to help investors make sustainable crypto investment decisions.

![Dashboard Preview](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)

## ✨ Features

### 📊 Real-Time Data
- **Live Cryptocurrency Prices**: Fetches real-time price data from CoinDCX API
- **Auto-Refresh**: Optional 30-second auto-refresh for live monitoring
- **Multiple Assets**: Tracks Bitcoin, Ethereum, Cardano, Polygon, Solana, and more

### 🌱 ESG Integration
- **Environmental Scores**: Energy consumption and sustainability metrics
- **Social Scores**: Community impact and social responsibility measures
- **Governance Scores**: Decentralization and governance quality assessment
- **Composite ESG Rating**: A-grade rating system (A+ to C)

### 💼 Portfolio Management
- **Custom Portfolio Input**: Configure your own cryptocurrency holdings
- **Portfolio Analytics**: Real-time portfolio value and allocation
- **Weighted ESG Scoring**: Portfolio-level ESG assessment based on holdings

### 📈 Advanced Visualizations
- **Interactive Charts**: Plotly-powered interactive visualizations
- **Portfolio Allocation**: Pie charts showing asset distribution
- **ESG Analysis**: Bar charts and scatter plots for ESG insights
- **Correlation Analysis**: ESG vs Price performance visualization

### 🎯 Key Metrics
- Portfolio value tracking
- Weighted ESG scores
- Environmental, Social, and Governance breakdowns
- ESG leaderboards and insights

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Internet connection for live data

### Installation

1. **Clone/Download the project**
   ```bash
   cd crypto-esg-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

## 📁 Project Structure

```
crypto-esg-dashboard/
├── app.py                 # Main Streamlit application
├── utils/
│   ├── coindcx_api.py    # CoinDCX API integration
│   └── esg_logic.py      # ESG calculation logic
├── data/
│   └── sample_esg_scores.csv  # ESG scores dataset
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🔧 Configuration

### Portfolio Setup
Use the sidebar to configure your cryptocurrency portfolio:
- Toggle "Use Custom Portfolio"
- Input your holdings for each supported cryptocurrency
- The dashboard will automatically calculate portfolio metrics

### Auto-Refresh
Enable auto-refresh in the sidebar for real-time monitoring (refreshes every 30 seconds).

## 📊 Data Sources

### Price Data
- **Source**: CoinDCX Public API
- **Endpoint**: `https://api.coindcx.com/exchange/ticker`
- **Update Frequency**: Real-time
- **Coverage**: Major cryptocurrencies (BTC, ETH, ADA, MATIC, SOL, etc.)

### ESG Data
- **Source**: Curated sample dataset (for demonstration)
- **Methodology**: Environmental, Social, and Governance factors
- **Scale**: 0-100 for each ESG component
- **Note**: Replace with certified ESG data for production use

## 🎨 Customization

### Adding New Cryptocurrencies
1. Add entries to `data/sample_esg_scores.csv`
2. Ensure the `market` column matches CoinDCX symbols
3. Provide ESG scores (0-100) for Environmental, Social, and Governance

### ESG Scoring Methodology
Current ESG factors include:
- **Environmental**: Energy consumption, consensus mechanism efficiency
- **Social**: Community governance, accessibility, financial inclusion
- **Governance**: Decentralization, transparency, development activity

### Styling and Themes
Modify `.streamlit/config.toml` to customize:
- Color schemes
- Layout preferences
- Default settings

## 🔍 Technical Details

### API Integration
- **Rate Limiting**: Built-in caching (30-second TTL)
- **Error Handling**: Graceful fallbacks and user notifications
- **Data Validation**: Automatic data type conversion and cleaning

### Performance Optimization
- **Caching**: Streamlit's `@st.cache_data` for API responses
- **Lazy Loading**: On-demand data processing
- **Efficient Rendering**: Optimized Plotly visualizations

### Security Considerations
- **No API Keys Required**: Uses public endpoints only
- **Data Privacy**: No personal data storage
- **Safe Defaults**: Reasonable default portfolio allocations

## 🚀 Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud
1. Fork this repository
2. Connect to Streamlit Cloud
3. Deploy directly from GitHub

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## 🔮 Future Enhancements

### Planned Features
- [ ] Historical ESG trend analysis
- [ ] ESG news feed integration
- [ ] Portfolio optimization based on ESG scores
- [ ] Risk assessment metrics
- [ ] CSV export functionality
- [ ] Email alerts for ESG threshold breaches
- [ ] Multi-currency support
- [ ] Advanced filtering and search

### Advanced Analytics
- [ ] ESG factor correlation analysis
- [ ] Volatility vs ESG score analysis
- [ ] Sector-wise ESG comparison
- [ ] Predictive ESG modeling

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional ESG data sources
- New visualization types
- Performance optimizations
- UI/UX enhancements
- Testing coverage

## ⚠️ Disclaimers

1. **ESG Data**: Current ESG scores are sample data for demonstration purposes. For production use, integrate with certified ESG rating providers.

2. **Investment Advice**: This tool is for informational purposes only and does not constitute financial or investment advice.

3. **Data Accuracy**: While we strive for accuracy, cryptocurrency prices are volatile and should be verified with multiple sources.

4. **Risk Warning**: Cryptocurrency investments carry high risk. Past performance does not guarantee future results.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **CoinDCX** for providing free cryptocurrency price data
- **Streamlit** for the amazing web app framework
- **Plotly** for interactive visualization capabilities
- **ESG Research Community** for sustainability metrics inspiration

---

**Built with ❤️ using Python, Streamlit, and modern data visualization libraries.**

For questions or support, please open an issue in the project repository.

# crypto-esg-dashboard
