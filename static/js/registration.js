$( function(){
    alert("Hello from Javascript");


$('#regform').submit(function() {
    var x = $('#pswrd').val();
    var y = $('#repswrd').val();
    if(x == y){
        return true;
    }
    else{
        alert("Your passwords do not match! Please re-enter them.");
        return false;
    }
});

});