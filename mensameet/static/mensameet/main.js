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

var membersFilter, topicsFilter, topicsFilterArr, mensaFilter, dateFilter, fullFilter;
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
    var dateTime = self.data('date-time');
      result = result && (self.data('date-time').indexOf(dateFilter)!==-1);
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

    if (fullFilter==true) {
        alert(self.data('members').length);
        alert(self.data("members-limit"));
        result = result && (self.data('members').length===self.data("members-limit"));
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

