const bar_chart_options = {
    scales: {
        yAxes: [{
            ticks: {
                beginAtZero: true,
                max: 100,
                stepSize: 10,
                fontStyle: 'bold',
                // fontColor: 'black',
                showLabelBackdrop: false
            },
            gridLines: {
                offsetGridLines: true,
                color: 'grey'
            }
        }],
        xAxes: [{
            ticks: {
                fontSize: 18,
                fontStyle: 'bold',
            }
        }]
    },
    tooltips: {
        enabled: false
    },
    legend: {
        position: 'bottom',
        fullWidth: true,
        labels: {
            fontSize: 20
        }
    },
    plugins: {
        labels: [{
            render: 'value',
            fontStyle: 'bold'
        }]
    }
}

function createChartjsBarChartData (bar_chart_data) {
    const m_background_color = [];
    const m_border_color = [];
    const u_background_color = [];
    const u_border_color = [];
    for (let i = 0; i < bar_chart_data["labels"].length; i++) {
        m_background_color.push('rgba(54, 162, 235, 0.2)');
        m_border_color.push('rgba(54, 162, 235, 1)');
        u_background_color.push('rgba(255, 99, 132, 0.2)');
        u_border_color.push('rgba(255, 99, 132, 1)');
    }

    // create chart.js data and return
    return {
        labels: bar_chart_data["labels"],
        datasets: [{
            label: 'memory usage %',
            data: bar_chart_data["memory_data"],
            backgroundColor: m_background_color,
            borderColor: m_border_color,
            borderWidth: 1
        }, {
            label: 'utilization %',
            data: bar_chart_data["utilization_data"],
            backgroundColor: u_background_color,
            borderColor: u_border_color,
            borderWidth: 1
        }]
    };
}
