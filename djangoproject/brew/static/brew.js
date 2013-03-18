time_mashing_started = null;
timer_timeout = null;
timer_active = false;
chart = null;

countdown_for_update = 25;

var options = {
    chart: {
        renderTo: 'mashing-tlog-graph',
        type: 'spline'
    },
    credits: {
        enabled: false
    },
    title: {
        text: null
    },

    xAxis: {
        type: 'datetime',
        dateTimeLabelFormats: { // don't display the dummy year
            month: '%e. %b',
            year: '%b'
        }
    },
    yAxis: {
        title: null,
//          max: 100,
//            min: 20,
        plotLines: [{
            value: 0,
            width: 3,
            color: '#EEEEEE'
        }]
    },
    legend: {
        enabled: false
    },
    exporting: {
        enabled: false
    },
    plotOptions: {
        series: {
            marker: {
                enabled: true
            }
        }
    },
    scrollbar: {
        enabled: true
    },
    tooltip: {
        formatter: function() {
            return '<b>'+ this.series.name +'</b><br/>'+
                this.x +': '+ this.y +'°C';
        }
    },
    series: [
        {
            name: 'Sensor 1',
            color: '#0088CC',
            data: []
        }
    ]
}


function render_realtime_data(data){
        // Update current live data
            // Update temperature label
        $('#temperature').text(data.temperature + '°');

        // Update heating label
        if(data.heat){
            $('.heating').fadeIn();
        }else{
            $('.heating').fadeOut();
        }


        // Update Mash Table
        index = data.active_mashingstep_index;
        state = data.active_mashingstep_state;
        
        switch (state){
        
            case 'finished':
                // Flag previous states and current as finished
                $('#mashingoverview tr:lt(' + (index + 1) + ')').removeClass('info').addClass('success').find('.status').text('Finished');
                break;
            case 'approach':
                // Flag previous states as finished
                $('#mashingoverview tr:lt(' + (index) + ')').removeClass('info').addClass('success').find('.status').text('Finished');
                // Flag current as approaching
                $('#mashingoverview tr:eq(' + index + ')').addClass('info').find('.status').text('Approaching...');
                break;
            case 'stay':
                // Flag previous states as finished
                $('#mashingoverview tr:lt(' + (index) + ')').removeClass('info').addClass('success').find('.status').text('Finished');
                // Flag current as stay
                $('#mashingoverview tr:eq(' + index + ')').addClass('info').find('.status').text('Running');
                break;
        }


}


/** ajax callback after start mashing executed **/
function mashing_started(data){
    check_response(data);

    chart_update_all();
    time_mashing_started = Date.now();
    timer_active = true;
    run_mashing();

    $('#mashing-start').addClass('disabled');
    $('#mashing-stop').removeClass('disabled');
}


/** function which fires mashing stop modal **/
function mashing_stop(data){
    check_response(data);

    timer_active = false;
    $('#mashing-start').removeClass('disabled');
    $('#mashing-stop').addClass('disabled');
}


/** ajax callback after stop mashing executed **/
function mashing_stopped(data){
    check_response(data);

    timer_active = false;
    $('#mashing-start').removeClass('disabled');
    $('#mashing-stop').addClass('disabled');
    $('#modalStopMashing').modal('hide')
}


function check_response(data){
    if(data.status != 200){
        alert ('something went wrong');
        console.log(data);
    }
}



// Load all data in graph, prolly only do this first time
function chart_update_all(){
    Dajaxice.brew.chart_update(callback_chart_update_all, {'batch_id' : Brew.batch_id});
}
function callback_chart_update_all(response){
    check_response(response);

    Brew.latest_mashlog_id = response.data.latest_mashlog_id;

    options.series[0].data = []
    for(item in response.data.chart){

        // Handle markers
        if(response.data.chart[item].icon != null){
            marker_settings = {enabled: true, symbol: 'url(/static/icons/' + response.data.chart[item].icon + '.png)'}
        }else{
            marker_settings = {enabled: false}
        }

        // Handle temperature/time
        options.series[0].data.push({
            y: parseFloat(response.data.chart[item].temperature),
            x: response.data.chart[item].seconds * 1000,
            marker: marker_settings
        });
    }

    render_realtime_data(response.data);

    // Show total runtime, will be overwritten when running, this is only to show total runtime after mashing
    
    time_string = (new Date).clearTime()
        .addSeconds(Brew.seconds_running)
        .toString('hh:mm:ss');
    $('#timer').text(time_string);

    chart = new Highcharts.Chart(options);
}

// Load latest data in graph
function chart_update_latest(){
    Dajaxice.brew.chart_update(callback_chart_update_latest, {'batch_id' : Brew.batch_id, 'greaterthan_mashlog_id' : Brew.latest_mashlog_id});
}
function callback_chart_update_latest(response){
    check_response(response);
    if (response.data.latest_mashlog_id != null){
        Brew.latest_mashlog_id = response.data.latest_mashlog_id;
    }

    options.series[0].data = []
    for(item in response.data.chart){
//        iso8601date = response.data.chart[item].seconds;
        // chart.series[0].addPoint([Date.parse(iso8601date), parseFloat(data.data.chart[item][1])]);

        // Handle markers
        if(response.data.chart[item].icon != null){
            marker_settings = {enabled: true, symbol: 'url(/static/icons/' + response.data.chart[item].icon + '.png)'}
        }else{
            marker_settings = {enabled: false}
        }
        point = {
            y: parseFloat(response.data.chart[item].temperature),
            x: response.data.chart[item].seconds * 1000,
            marker: marker_settings
        };

        chart.series[0].addPoint(point);
    }

render_realtime_data(response.data);



}





function run_mashing(){

// Update timer
    seconds_passed = (Date.now() - time_mashing_started) / 1000;
    time_string = (new Date).clearTime()
        .addSeconds(seconds_passed)
        .toString('hh:mm:ss');
    $('#timer').text(time_string);

    if(timer_active){
        timer_timeout=setTimeout("run_mashing()",200);
    }

    countdown_for_update = countdown_for_update - 1;
    if(countdown_for_update < 1){
        countdown_for_update = 11;
        chart_update_latest();
    }


}




function delete_mashing_data_callback(data){
    alert('Mash data deleted');
    chart_update_all();
}