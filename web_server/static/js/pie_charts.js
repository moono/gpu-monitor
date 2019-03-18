const pieBGColors = [
    'rgba(252, 161, 125, 1)',
    'rgba(154, 52, 142, 1)',
    'rgba(232, 219, 125, 1)',
    'rgba(255, 159, 64, 1)',
    'rgba(153, 102, 255, 1)',
    'rgba(255, 99 132, 1)',
    'rgba(75, 192, 192, 1)',
    'rgba(255, 206, 86, 1)',
    'rgba(54, 162, 235, 1)',
    'rgba(249, 219, 189, 1)',
    'rgba(218, 98, 125, 1)',
    'rgba(85, 140, 140, 1)',
];

const pie_chart_options_tooltips = {
    enabled: false
};

const maxLabelLength = 15;
const pie_chart_options_legend = {
    position: 'left',
    fullWidth: true,
    labels: {
        fontSize: 20,
        fontStyle: 'bold',
        usePointStyle: true,
        filter : function (legendItem, cdata) {
            // update long labels
            let label = legendItem.text;
            let label_candidates = label.split(/[-_/]+/);
            let isFound = false;
            for (let j = 0; j < user_names.length; j++) {
                for (let k = 0; k < label_candidates.length; k++) {
                    if (label_candidates[k].indexOf(user_names[j]) === 0) {
                        legendItem.text = label.substring(0, label.indexOf('/')) + '/' + user_names[j];
                        isFound = true;
                        break;
                    }
                }

                if (isFound) {
                    break;
                }
            }

            // check if not found appropriate string (user_name) to filter,
            // cut string into fixed length
            if (!isFound) {
                legendItem.text = label.slice(0, maxLabelLength);
            }
            return true;
        }
    }
};

const pie_chart_options_plugins = {
    labels: [
        {
          render: 'label',
          fontColor: '#000',
          fontStyle: 'bold',
          arc: false,
          position: 'outside'
        },
        {
          render: 'percentage',
          fontColor: '#000',
          fontStyle: 'bold',
          textShadow: true,
          position: 'deafult',
          precision: 2
        }
    ]
};

const pie_chart_options = {
    tooltips: pie_chart_options_tooltips,
    legend: pie_chart_options_legend,
    plugins: pie_chart_options_plugins
}


function createChartjsPieChartData (pie_chart_data, removeFreeMemory) {
    // prepare variables
    let labelsData = pie_chart_data["labels"];
    let pointsData = pie_chart_data["processes_data"];
    if (removeFreeMemory) {
        const dataLength = pie_chart_data["labels"].length;
        labelsData = labelsData.slice(0, dataLength - 1);
        pointsData = pointsData.slice(0, dataLength - 1);
    }

    // set same color for same gpu index
    const background_color = [];
    for (let i = 0; i < labelsData.length; i++) {
        let label = labelsData[i];
        let index = 0;
        for (let j=0; j<pieBGColors.length; j++) {
            if (label.indexOf('gpu_' + j) == 0) {
                index = j;
                break;
            }
        }
        background_color.push(pieBGColors[index]);
    }

    // create chart.js data and return
    return {
        labels: labelsData,
        datasets: [{
            label: labelsData,
            data: pointsData,
            backgroundColor: background_color
        }]
    };
}
