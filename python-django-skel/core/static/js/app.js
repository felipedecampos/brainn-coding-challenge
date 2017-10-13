$(document).ready(function() {
    var repository_table = $('#repository-table');
     repository_table.dataTable({
         "processing": true,
         "ajax": {
             "processing": true,
             "url": repository_table.attr('data-url'),
             "dataSrc": "",
             "deferRender": true
         },
         "columns": [
             { "data": "pk", "searchable": false },
             { "data": "fields.username", "searchable": false },
             { "data": "fields.repository_id", "searchable": false },
             { "data": "fields.name", "searchable": false },
             { "data": "fields.url", "searchable": false },
             { "data": "fields.languages", "searchable": false },
             { "data": "fields.tags" }
         ],
         "oLanguage": {
             "sSearch": "Search by TAGs"
         }
     });
 });
