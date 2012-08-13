time_mashing_started = null;
timer_timeout = null;
timer_active = false;

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