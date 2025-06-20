document.addEventListener('DOMContentLoaded', function () {
    // Get data from canvas elements
    const categoryCanvas = document.getElementById('categoryPieChart');
    const monthlyCanvas = document.getElementById('monthlyBarChart');
    
    if (!categoryCanvas || !monthlyCanvas) return;
    
    // Get theme-aware text color from the body for charts
    const bodyTextColor = getComputedStyle(document.body).getPropertyValue('color');

    const categoryLabels = JSON.parse(categoryCanvas.dataset.labels || '[]');
    const categoryValues = JSON.parse(categoryCanvas.dataset.values || '[]');
    const monthlyLabels = JSON.parse(monthlyCanvas.dataset.labels || '[]');
    const monthlyValues = JSON.parse(monthlyCanvas.dataset.values || '[]');
    const currency = categoryCanvas.dataset.currency || 'VND';

    // Calculate total for percentage calculations
    const totalExpenses = categoryValues.reduce((sum, value) => sum + value, 0);

    const categoryCtx = categoryCanvas.getContext('2d');
    if (categoryValues.length > 0) {
        new Chart(categoryCtx, {
            type: 'pie',
            data: {
                labels: categoryLabels,
                datasets: [{
                    label: 'Expenses by Category',
                    data: categoryValues,
                    backgroundColor: [
                        '#2E93fA', '#66DA26', '#546E7A', '#E91E63', '#FF9800',
                        '#9C27B0', '#4CAF50', '#FFC107', '#795548', '#607D8B'
                    ],
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { 
                        position: 'top',
                        labels: {
                            color: bodyTextColor, // Use theme-aware text color
                            generateLabels: function(chart) {
                                const data = chart.data;
                                if (data.labels.length && data.datasets.length) {
                                    return data.labels.map((label, i) => {
                                        const value = data.datasets[0].data[i];
                                        const percentage = totalExpenses > 0 ? ((value / totalExpenses) * 100).toFixed(1) : 0;
                                        return {
                                            text: `${label}: ${percentage}% (${value.toLocaleString()} ${currency})`,
                                            fillStyle: data.datasets[0].backgroundColor[i],
                                            strokeStyle: data.datasets[0].backgroundColor[i],
                                            lineWidth: 0,
                                            hidden: false,
                                            index: i
                                        };
                                    });
                                }
                                return [];
                            }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const value = context.raw;
                                const percentage = totalExpenses > 0 ? ((value / totalExpenses) * 100).toFixed(1) : 0;
                                return `${context.label}: ${percentage}% (${value.toLocaleString()} ${currency})`;
                            }
                        }
                    }
                }
            }
        });
    }

    const monthlyCtx = monthlyCanvas.getContext('2d');
    if (monthlyValues.length > 0) {
        new Chart(monthlyCtx, {
            type: 'bar',
            data: {
                labels: monthlyLabels,
                datasets: [{
                    label: `Total Spending per Month (${currency})`,
                    data: monthlyValues,
                    backgroundColor: '#66DA26'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: bodyTextColor, // Use theme-aware text color for Y-axis
                            callback: function(value) {
                                return value.toLocaleString();
                            }
                        }
                    },
                    x: {
                        ticks: {
                            color: bodyTextColor // Use theme-aware text color for X-axis
                        }
                    }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.raw.toLocaleString()} ${currency}`;
                            }
                        }
                    }
                }
            }
        });
    }
});
