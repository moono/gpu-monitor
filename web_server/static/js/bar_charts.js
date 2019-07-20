const bar_chart_options_scales = {
    yAxes: [{
        ticks: {
            beginAtZero: true,
            max: 100,
            //min: 0,
            stepSize: 10,
            fontStyle: 'bold',
            // fontColor: 'white',
            fontColor: 'rgba(255, 255, 255, 0.7)',
            showLabelBackdrop: false
        },
        gridLines: {
            offsetGridLines: true,
            color: 'rgba(255, 255, 255, 0.2)'
        }
    }],
    xAxes: [{
        ticks: {
            fontSize: 18,
            fontStyle: 'bold',
            // fontColor: 'white'
            fontColor: 'rgba(255, 255, 255, 0.7)'
        }
    }]
};

const bar_chart_options_tooltips = {
    enabled: false
};

const bar_chart_options_legend = {
    position: 'bottom',
    fullWidth: true,
    labels: {
        fontSize: 20,
        // fontColor: 'white'
        fontColor: 'rgba(255, 255, 255, 0.7)'
    }
};

const bar_chart_options_plugins = {
    labels: [
        {
            render: 'value',
            fontStyle: 'bold'
        }
    ]
};

const bar_chart_options = {
    scales: bar_chart_options_scales,
    tooltips: bar_chart_options_tooltips,
    legend: bar_chart_options_legend,
    plugins: bar_chart_options_plugins
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
