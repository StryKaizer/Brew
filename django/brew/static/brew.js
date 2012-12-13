time_mashing_started = null;
timer_timeout = null;
timer_active = false;
chart = null;

var options = {
  chart: {
    renderTo: 'mashing-tlog-graph',
    type: 'spline',

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




      /** ajax callback after start mashing executed **/
      function mashing_started(data){
        check_response(data);

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
        Dajaxice.brew.chart_update_all(callback_chart_update_all);
      }
      function callback_chart_update_all(data){
        check_response(data);
            // Define the data points. All series have a dummy year
            // of 1970/71 in order to be compared on the same x axis. Note
            // that in JavaScript, months start at 0 for January, 1 for February etc.


        options.series[0].data = [
            [Date.UTC(2012,  2, 11, 0,0,0), 25.4],
            [Date.UTC(2012,  2, 11, 0,0,5), 25.8],
            [Date.UTC(2012,  2, 11, 0,0,15), 26.8],
            [Date.UTC(2012,  2, 11, 0,0,25), 25.8],
            [Date.UTC(2012,  2, 11, 0,0,30), 25.8],
            [Date.UTC(2012,  2, 11, 0,0,35), 28.8]
            ]
          chart = new Highcharts.Chart(options); 
      }

      // Load latest data in graph
      function chart_update_latest(){
        Dajaxice.brew.chart_update_latest(callback_chart_update_latest);
      }
      function callback_chart_update_latest(data){
        check_response(data);

        chart.series[0].addPoint([Date.UTC(2012,  2, 11, 0,0,40), 22.8]);
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


}