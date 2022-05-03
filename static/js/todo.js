$( function(){

    $(':checkbox').change(function(){
        var todo_id = $(this).attr('id');
        var item = document.getElementById(todo_id+'')
        if(this.checked){
            $.ajax({
                url:"/updatetodone",
                method:"POST",
                data:{"todo_id":todo_id},
                success:function(data)
                {
                    location.reload();
                }
           
            });
        }
        else{
            $.ajax({
                url:"/updatetonone",
                method:"POST",
                data:{"todo_id":todo_id,"done":0},
                success:function(data)
                {
                    location.reload();
                }
           
            });
        }
    });
    

    $('#addItem').submit(function() {
        return false;
    });

    $('#submit').click(function(){
        
        
        $.ajax({
            url:"/additem",
            method:"POST",
            data: $("#addItem").serialize(),
            success:function(data)
            {
                location.reload();
            }
       
        });

    })
    
    
    
    
    
});
