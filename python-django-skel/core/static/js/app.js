$(document).ready(function() {
    $('#repository-table').dataTable({
        "processing": true,
         "ajax": {
             "processing": true,
             "url": $('#repository-table').data('url'),
             "dataSrc": ""
         },
         "columns": [
             { "data": "pk", "searchable": false },
             { "data": "fields.repository_id", "searchable": false },
             { "data": "fields.name", "searchable": false },
             { "data": "fields.url", "searchable": false },
             { "data": "fields.languages", "searchable": false },
             { "data": "fields.tags", "searchable": true },
             { "data": "fields.repository_id", "searchable": false }
         ],
         "columnDefs": [{
              "targets": 5,
              "render": function ( data, type, row, meta ) {
                  if (data !== "") {
                      var labels        = String(data).toLowerCase().split(/\s*,\s*/).filter(function(value) { return value });
                      var delete_link   = '/delete';
                      var delete_btn    = '<a href="' + delete_link + '" class="btn btn-xs text-danger delete-tag" data-repository-id="'+row.fields.repository_id+'">' +
                          '<span class="glyphicon glyphicon-trash"></span>' +
                          '</a>';
                      var before_label  = '<span class="label label-info">';
                      var after_label   = delete_btn + '</span> ';
                      var rtn = '';

                      for (var label in labels) {
                          if ($.trim(label) !== "") {
                              rtn += before_label + $.trim(labels[label]) + after_label;
                          }
                      }

                      return rtn;
                  }
                  return data;
              }
          },
         {
              "targets": 6,
              "render": function ( data, type, row, meta ) {
                  return '<button type="button" class="btn btn-success" data-toggle="modal" data-target="#add-tags-modal" data-repository-id="'+data+'">' +
                      'Add tags' +
                      '</button>';
              }
          }],
         "oLanguage": {
             "sSearch": "Search by TAGs"
         }
    });
});

$('#add-tags-modal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var repository_id = button.data('repository-id');
    var modal = $(this);

    modal.find('.modal-title').text('Add tags to: ' + button.parent().parent().find('>:nth-child(3)').text());
    modal.find('.modal-body #repository-id, .modal-body #tags').val("");
    modal.find('.modal-body #repository-id').val(repository_id);
});

$(document).on('click', '.add-new-tags', function() {
    var csrfmiddlewaretoken = $('*[name=csrfmiddlewaretoken]').val();
    var repository_id       = $('#repository-id').val();
    var tags                = $('#tags').val();
    var repository_add_tags = $('#add-tags-modal').data('url');

    $.ajax({
        url: repository_add_tags,
        type:'POST',
        dataType: 'json',
        data: {
            csrfmiddlewaretoken: csrfmiddlewaretoken,
            repository_id: repository_id,
            tags: tags
        },
        success:function(data) {
            $('#add-tags-modal .modal-body').html('<p>' + data.msg + '</p>');
            $('#add-tags-modal .modal-footer .add-new-tags').remove();
            $(document).on('click', '#add-tags-modal *[data-dismiss="modal"]', function(){
                window.location.reload();
            });
            $('#add-tags-modal').on('hidden.bs.modal', function () {
                window.location.reload();
            });
        }
    });
});

$(document).on('click', '.delete-tag', function(e) {
    e.preventDefault();
    var repository_del_tag  = $('#repository-table').data('delete-url');
    var self                = $(this);
    var repository_id       = self.data('repository-id');
    var tag                 = self.parent().text();
    var csrfmiddlewaretoken = $('*[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url: repository_del_tag,
        type:'POST',
        dataType: 'json',
        data: {
            csrfmiddlewaretoken: csrfmiddlewaretoken,
            repository_id: repository_id,
            tag: tag
        },
        success:function(data) {
            window.location.reload();
        }
    });
});