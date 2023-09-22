



const alertPlaceholder = document.getElementById('liveAlertPlaceholder')
const appendAlert = (message, type) => {
  const wrapper = document.createElement('div')
  wrapper.innerHTML = [
    `<div class="alert alert-${type} alert-dismissible" role="alert">`,
    `   <div>${message}</div>`,
    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
    '</div>'
  ].join('')

  alertPlaceholder.append(wrapper)
}

const alertTrigger = document.getElementById('liveAlertBtn')
if (alertTrigger) {
  alertTrigger.addEventListener('click', () => {
    appendAlert('Nice, you triggered this alert message!', 'success')
  })
}




//department tasks post handling ajax functions


function department_task_complete_ajax (e) {
    var member_id = $(this).attr('member_id');
    e.preventDefault();

    $.ajax({
        type:'POST',
        url: "/tasks",
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            name:'department_task_complete',
            id:member_id,
            success: function() { 
                setTimeout(function(){
                    location.reload(); 
                }, 1500);
                $('#liveAlertBtn').html(appendAlert('Nice, you triggered this alert message!', 'success')); 
         
    },},
})

};

function department_task_on_progress_ajax (e) {
    var member_id = $(this).attr('member_id');
    e.preventDefault();

    $.ajax({
        type:'POST',
        url: "/tasks",
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            name:'department_task_on_progress',
            id:member_id,
            success: function() { 
                setTimeout(function(){
                    location.reload(); 
                }, 1500);
                $('#liveAlertBtn').html(appendAlert('Nice, you triggered this alert message!', 'warning')); 
         
    },},
})

};
function department_task_delete_ajax (e) {
    var member_id = $(this).attr('member_id');
    e.preventDefault();

    $.ajax({
        type:'POST',
        url: "/tasks",
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            name:'department_task_delete',
            id:member_id,
            success: function() { 
                setTimeout(function(){
                    location.reload(); 
                }, 1500);
                $('#liveAlertBtn').html(appendAlert('Nice, you triggered this alert message!', 'danger')); 
         
    },},
})

};




//personal tasks post handling ajax functions
function add_task_ajax (e)  {
    e.preventDefault();
    $.ajax({
        type:'POST',
        url: "/tasks",
        data: {
            title: $('#title').val(),
            content: $('#content').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            name: 'submit_new_task',


        },
        success:function(data){
            $('#success').html("as")
            location.reload(true)
            
        }
    })

};

function complete_task_ajax (e)  {
    var member_id = $(this).attr('member_id');
    e.preventDefault();
    $.ajax({
        type:'POST',
        url: "/tasks",
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            name:'complete_task_form',
            id:member_id,
            success: function() { 
                setTimeout(function(){
                    location.reload(); 
                }, 1500);
                $('#liveAlertBtn').html(appendAlert('Nice, you triggered this alert message!', 'success')); 
         
    },},

})


};







function on_progress_task_ajax (e)  {
    var member_id = $(this).attr('member_id');
    e.preventDefault();

    $.ajax({
        type:'POST',
        url: "/tasks",
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            name:'task_on_progress',
            id:member_id,
            success: function() { 
                setTimeout(function(){
                    location.reload(); 
                }, 1500);
                $('#liveAlertBtn').html(appendAlert('Nice, you triggered this alert message!', 'warning')); 
    },}
})

};

function task_delete_ajax (e) {
    var member_id = $(this).attr('member_id');
    e.preventDefault();

    $.ajax({
        type:'POST',
        url: "/tasks",
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            name:'task_delete',
            id:member_id,
            success: function() { 
                setTimeout(function(){
                    location.reload(); 
                }, 1500);
                $('#liveAlertBtn').html(appendAlert('Nice, you triggered this alert message!', 'danger')); 
    },}

    })
}
;



//lead  post handling ajax functions

function lead_complete_ajax (e) {
    var member_id = $(this).attr('member_id');
    e.preventDefault();

    $.ajax({
        type:'POST',
        url: "/tasks",
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            name:'lead_complete',
            id:member_id,
            success: function() { 
                setTimeout(function(){
                    location.reload(); 
                }, 1500);
                $('#liveAlertBtn').html(appendAlert('Nice, you triggered this alert message!', 'success')); 
    },}
})

};


function lead_on_progress_ajax (e) {
    e.preventDefault();
    var member_id = $(this).attr('member_id');

    $.ajax({
        type:'POST',
        url: "/tasks",
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            name:'lead_on_progress',
            id:member_id,
            success: function() { 
                setTimeout(function(){
                    location.reload(); 
                }, 1500);
                $('#liveAlertBtn').html(appendAlert('Nice, you triggered this alert message!', 'warning')); 
    },}
})

};