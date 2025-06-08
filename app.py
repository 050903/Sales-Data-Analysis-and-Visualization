from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

app = Flask(__name__)

# Load the data
data = pd.read_csv('sales_data_complex.csv')

@app.route('/')
def index():
    # Create a combined visualization with three subplots
    fig = plt.figure(figsize=(18, 16))
    gs = fig.add_gridspec(3, 1, height_ratios=[1, 1, 1])

    # Grouped Bar Chart: Revenue by Product and Region for Q1 and Q2
    ax0 = fig.add_subplot(gs[0])
    sns.barplot(data=data, x='Khu vực', y='Doanh số', hue='Sản phẩm', ax=ax0, ci=None, order=data['Khu vực'].unique())
    ax0.set_title('Grouped Bar Chart of Revenue by Product and Region for Q1 and Q2')
    ax0.set_xlabel('Region')
    ax0.set_ylabel('Revenue')
    ax0.legend(title='Product')

    # Line Chart: Revenue Trend by Quarter for Each Region
    ax1 = fig.add_subplot(gs[1])
    sns.lineplot(data=data, x='Quý', y='Doanh số', hue='Khu vực', marker='o', ax=ax1)
    ax1.set_title('Revenue Trend by Quarter for Each Region')
    ax1.set_xlabel('Quarter')
    ax1.set_ylabel('Revenue')
    ax1.legend(title='Region')

    # Stacked Bar Chart: Profit Margins by Product and Region
    ax2 = fig.add_subplot(gs[2])
    profit_data = data.groupby(['Khu vực', 'Sản phẩm'])['Lợi nhuận'].sum().unstack()
    profit_data.plot(kind='bar', stacked=True, ax=ax2)
    ax2.set_title('Profit Margins by Product and Region')
    ax2.set_xlabel('Region')
    ax2.set_ylabel('Profit')
    ax2.legend(title='Product')

    plt.tight_layout()

    # Save the combined plot to a BytesIO object
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    # Convert the summary data to HTML
    summary_data = data.groupby(['Khu vực', 'Quý']).agg({
        'Doanh số': 'sum',
        'Chi phí': 'sum',
        'Lợi nhuận': 'sum'
    }).reset_index()
    summary_html = summary_data.to_html(classes='table table-striped', index=False)

    return render_template('index.html', plot_url=plot_url, summary_html=summary_html)

if __name__ == '__main__':
    app.run(debug=True)
