



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
};



// changes the sided navbar from big to small
function trigger_small_navbar (e){
    e.preventDefault();
    $('#small_off_canvas').attr('class','offcanvas offcanvas-start show');
    $('#big_off_canvas').attr('class','offcanvas offcanvas-start hide');

}

function trigger_big_navbar (e){
    e.preventDefault();
    $('#big_off_canvas').attr('class','offcanvas offcanvas-start show');
    $('#small_off_canvas').attr('class','offcanvas offcanvas-start hide');
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
                }, 2000);
                $('#liveAlertBtn').html(appendAlert('Department Task completed successfully', 'success')); 
         
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
                }, 2000);
                $('#liveAlertBtn').html(appendAlert('You have changed the Department Task status to "on progress"', 'warning')); 
         
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
                }, 2000);
                $('#liveAlertBtn').html(appendAlert('You have Deleted the Department Task Successfully', 'danger')); 
         
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
            description: $('#description').val(),
            additional_description:$('#additional_description').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            name: 'submit_new_task',


        },
        success:function(data){
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
                }, 2000);
                $('#liveAlertBtn').html(appendAlert('Task completed successfully', 'success')); 
         
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
                }, 2000);
                $('#liveAlertBtn').html(appendAlert('You have changed the Task status to "on progress"', 'warning')); 
  },},
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
                }, 2000);
                $('#liveAlertBtn').html(appendAlert('You have Deleted the Task Successfully', 'danger')); 
    },},
})

};



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
                }, 2000);
                $('#liveAlertBtn').html(appendAlert('Lead completed successfully', 'success')); 

    },},
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
                }, 2000);
                $('#liveAlertBtn').html(appendAlert('You have changed the Lead status to "on progress"', 'warning')); 
    },},
})

};


function lead_delete_ajax (e) {
    var member_id = $(this).attr('member_id');
    e.preventDefault();

    $.ajax({
        type:'POST',
        url: "/tasks",
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            name:'lead_delete',
            id:member_id,
            success: function() { 
                setTimeout(function(){
                    location.reload(); 
                }, 2000);
                $('#liveAlertBtn').html(appendAlert('You have Deleted the Lead Successfully', 'danger')); 
    },},
})

};





function add_lead_ajax (e)  {
    e.preventDefault();
    $.ajax({
        type:'POST',
        url: "/tasks",
        data: {
            title:$('#lead_title').val(),
            description: $('#lead_description').val(),
            costumer_name:$('#costumer_name').val(),
            costumer_id:$('#costumer_id').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            name: 'submit_new_lead',


        },
        success:function(data){
            location.reload(true)
            
        }
    })

};



$(document).ready(function(){
    var cur = 4;
    $('.task_col').hide();
    $('.task_col').slice(0,4).show();
    $('.load_more_task').click(function(){
        cur += 4
        $('.task_col').slice(0,cur).show();
        // $(this).fadeOut();
        console.log(cur)
    });

});



$(document).ready(function(){
    var cur = 4;
    $('.lead_col').hide();
    $('.lead_col').slice(0,4).show();
    $('.load_more_lead').click(function(){
        cur += 4
        $('.lead_col').slice(0,cur).show();
        console.log(cur)
    });

});


$(document).ready(function(){
    var cur = 4;
    $('.department_task_col').hide();
    $('.department_task_col').slice(0,4).show();
    $('.load_more_department_task').click(function(){
        cur += 4
        $('.department_task_col').slice(0,cur).show();
        // $(this).fadeOut();
        console.log(cur)
    });

});



$('.close_small_navbar').on('click',trigger_big_navbar)

$('.close_big_navbar').on('click',trigger_small_navbar)

$('.department_task_complete_button').on('click',department_task_complete_ajax)


$('.department_task_on_progress_button').on('click',department_task_on_progress_ajax)


$('.department_task_delete_button').on('click',department_task_delete_ajax)


$(document).on('submit','#add_task_submit_form',add_task_ajax)


$('.task_complete_button').on('click',complete_task_ajax)


$('.task_on_progress_button').on('click',on_progress_task_ajax)


$('.task_delete_button').on('click',task_delete_ajax)


$(document).on('submit','#add_lead_submit_form',add_lead_ajax)



$('.lead_complete_button').on('click',lead_complete_ajax)


$('.lead_on_progress_button').on('click',lead_on_progress_ajax)


$('.lead_delete_button').on('click',lead_delete_ajax)

