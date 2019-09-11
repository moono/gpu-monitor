const pieBGColors = [
    'rgba(252, 161, 125, 0.2)',
    'rgba(154, 52, 142, 0.2)',
    'rgba(232, 219, 125, 0.2)',
    'rgba(255, 159, 64, 0.2)',
    'rgba(153, 102, 255, 0.2)',
    'rgba(255, 99 132, 0.2)',
    'rgba(75, 192, 192, 0.2)',
    'rgba(255, 206, 86, 0.2)',
    'rgba(54, 162, 235, 0.2)',
    'rgba(249, 219, 189, 0.2)',
    'rgba(218, 98, 125, 0.2)',
    'rgba(85, 140, 140, 0.2)',
];

const pieBRColors = [
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

const pie_chart_options = {
    tooltips: {
        enabled: false
    },
    legend: {
        position: 'left',
        fullWidth: true,
        labels: {
            fontSize: 20,
            fontStyle: 'bold',
            usePointStyle: true,
            filter : function (legendItem, cdata) {
                // update long labels
                const maxLabelLength = 15;

                // get current display text
                let label = legendItem.text;

                // split label into list of strings with '-', '_', '/'
                let label_candidates = label.split(/[-_/]+/);
                let isFound = false;
                for (let i = 0; i < label_candidates.length; i++) {
                    for (let key in user_names) {
                        if (label_candidates[i] === key) {
                            legendItem.text = label.substring(0, label.indexOf('/')) + '/' + user_names[key];
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
    },
    plugins: {
        labels: [{
            render: 'label',
            fontStyle: 'bold',
            arc: false,
            position: 'outside'
        },
        {
            render: 'percentage',
            fontStyle: 'bold',
            textShadow: true,
            position: 'deafult',
            precision: 2
        }]
    }
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
    const border_color = [];
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
        border_color.push(pieBRColors[index]);
    }

    // create chart.js data and return
    return {
        labels: labelsData,
        datasets: [{
            label: labelsData,
            data: pointsData,
            backgroundColor: background_color,
            borderColor: border_color
        }]
    };
}
