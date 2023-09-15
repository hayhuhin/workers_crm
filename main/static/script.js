
function add_task_ajax (e)  {

    e.preventDefault();
    $.ajax({
        type:'POST',
        url: "/tasks",
        data: {
            title: $('#title').val(),
            content: $('#content').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            name: "add_task",


        },
        success:function(data){
            $('#success').html("as")
            location.reload(true)
            
        }
    })

}