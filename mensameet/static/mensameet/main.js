var coll = document.getElementsByClassName("collaps");
var i;
for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    var content = document.getElementById("allFilter");
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}

var field_username = document.getElementById("id_username");
var tool_user = document.getElementById("tooltip-username");
  field_username.addEventListener("focus", function() {
      tool_user.style.display = "block";
  });
  field_username.addEventListener("blur", function() {
        tool_user.style.display = "none";
  });

var field_password = document.getElementById("id_password1");
var tool_password = document.getElementById("tooltip-password");
  field_password.addEventListener("focus", function() {
      tool_password.style.display = "block";
  });
  field_password.addEventListener("blur", function() {
        tool_password.style.display = "none";
  });


var field_password2 = document.getElementById("id_password2");
var tool_password2 = document.getElementById("tooltip-password2");
  field_password2.addEventListener("focus", function() {
      tool_password2.style.display = "block";
  });
  field_password2.addEventListener("blur", function() {
        tool_password2.style.display = "none";
  });

var membersFilter, topicsFilter, topicsFilterArr, mensaFilter, dateFilter, timeFilterBefore, timeFilterAfter;
function updateFilters() {
  $('.task-list-row').hide().filter(function() {
    var
      self = $(this),
      result = true;

    if (membersFilter && (membersFilter != 'Show All')) {
      result = result && membersFilter === self.data('members-limit');
    }

    if (mensaFilter && (mensaFilter != 'Show All')) {
      result = result && mensaFilter === self.data('mensa');
    }

    if (dateFilter && (dateFilter != '')) {
    var dateTime = self.data('date');
      result = result && (self.data('date').indexOf(dateFilter)!==-1);
    }

    if (timeFilterBefore && timeFilterBefore!=='' && timeFilterAfter && timeFilterAfter !== '') {
            selectedTime = parseInt(self.data('time').replace(':', ''));
            result = result && (selectedTime<=parseInt(timeFilterBefore)) && (selectedTime>=parseInt(timeFilterAfter));
        }


    if (self.data('topics') == '' && topicsFilterArr!='') {
    result = false;
    }

    if (topicsFilter && topicsFilterArr!='') {

        var tr=true;
        var i;
        for (i=0;i<topicsFilterArr.length;i++) {

            if (self.data('topics').indexOf(topicsFilterArr[i]) == -1) {
                tr = false;
                break;
            }
        }
            result = result && tr;
    }

    return result;
  }).show();

}

function getValue( elem ) {
    var a ="";
    elem.each(function( index ) {
        let b = $( this ).text();
        a = a.concat(b);
        a = a.concat(",");
    });
    a = a.slice(0,-1);
    return a;
}

$('#topics-filter').on('change', function() {
    topicsFilter = getValue($("div.dropdown-menu.show div.inner ul li.selected"));
    topicsFilterArr = topicsFilter.split(",");
    updateFilters();
    });

$('#members-limit-filter').on('change', function() {
    membersFilter = $('select[id="members-limit-filter"] :selected').attr('data-filter-value');
    updateFilters();
});

$('#mensa-filter').on('change', function() {
    mensaFilter = $('select[id="mensa-filter"] :selected').val();
    updateFilters();
});

$('#date-filter').on('change', function() {
    dateFilter=$('#date-filter').val();
    updateFilters();

});

$('.clear-date').on('click', function() {
    $('.date').datepicker('setDate', null);
    dateFilter='';
    updateFilters();
});

$('#time-filter').on('change', function() {
    timeFilterBefore=$('select[id="time-filter"] :selected').attr('data-time-before');
    timeFilterAfter=$('select[id="time-filter"] :selected').attr('data-time-after');
    updateFilters();
});
