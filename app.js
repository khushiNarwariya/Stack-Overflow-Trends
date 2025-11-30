// Function to fetch data from our API
async function fetchChartData() {
    try {
        const response = await fetch('http://127.0.0.1:5500/api/data');
        // https://narwariya1234khushi.pythonanywhere.com/api/data'
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching chart data:', error);
        return null;
    }
}

// Function to create the chart
async function createChart() {
    const chartData = await fetchChartData();
    
    if (!chartData) {
        console.error('No data available to create chart');
        return;
    }
    
    // Get the canvas element
    const ctx = document.getElementById('myChart').getContext('2d');
    
    // Create the chart
    new Chart(ctx, {
        type: 'bar', // Can be changed to 'line', 'pie', etc.
        data: chartData,
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Sales Data 2023'
                }
            }
        }
    });
}

// Initialize the chart when the page loads
document.addEventListener('DOMContentLoaded', createChart);