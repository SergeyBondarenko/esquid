$(function() {

// Send vars from menu to backend
var sendVarsToBackend = function(vars, callback){
	$.ajax({
	  type: 'POST',
	  url: 'postmenu/',
	  data: {
	  	//msg: 'Hello my friend!',
	  	msg: vars,
	  },
	  success: function(response){
		callback(response);
	  	console.log('Successful response from backend!');
	  },
	  error: function(response){
	  	console.log('Error (ajax post): Unable to receive data from server.');
	  }
	}); // ajax post
}

// Init menu
var initSelectableTree = function() {
  return $('#treeview-selectable').treeview({
  	color: "#428bca",
	data: menuItems,
    multiSelect: $('#chk-select-multi').is(':checked'),
    onNodeSelected: function(event, node) {
      //$('#selectable-output').append('<p>' + node.text + ' was selected</p>');
      //$('#selectable-output').append('( '+node.parents+ '.' +node.text+ '="hello")');
	  sendVarsToBackend(node.text, function(){
	  	console.log(node.text);
	  });
    },
    onNodeUnselected: function (event, node) {
      //$('#selectable-output').append('<p>' + node.text + ' was unselected</p>');
	  console.log(node.text);
    }
  });
};

// Build menu
var menuItems = {};
var buildMenu = function(){
	$.getJSON("/static/esearch/json/test_menu.json", function(menu_data){
		//console.log("Success: Menu json will be used.");
	})
	.done(function(menu_data){
		menuItems = JSON.stringify(menu_data);
		//console.log(menuItems);
		initSelectableTree()
	})
	.fail(function(){
		console.log("Fail: Menu json was not used.");
	})
	.always(function(){
		//console.log("Complete: Finished taking menu.");
	});
};
buildMenu();


var $selectableTree = initSelectableTree();

// Form functionality
var findSelectableNodes = function() {
  return $selectableTree.treeview('search', [ $('#input-select-node').val(), { ignoreCase: false, exactMatch: false } ]);
};
var selectableNodes = findSelectableNodes();

$('#chk-select-multi:checkbox').on('change', function () {
  console.log('multi-select change');
  $selectableTree = initSelectableTree();
  selectableNodes = findSelectableNodes();          
});

// Select/unselect/toggle nodes
$('#input-select-node').on('keyup', function (e) {
  selectableNodes = findSelectableNodes();
  $('.select-node').prop('disabled', !(selectableNodes.length >= 1));
});

$('#btn-select-node.select-node').on('click', function (e) {
  //$selectableTree.treeview('selectNode', [ selectableNodes, { silent: $('#chk-select-silent').is(':checked') }]);
});

$('#btn-unselect-node.select-node').on('click', function (e) {
  //$selectableTree.treeview('unselectNode', [ selectableNodes, { silent: $('#chk-select-silent').is(':checked') }]);
});

$('#btn-toggle-selected.select-node').on('click', function (e) {
  //$selectableTree.treeview('toggleNodeSelected', [ selectableNodes, { silent: $('#chk-select-silent').is(':checked') }]);
});

// Clear query field
$('#clear-query-field.select-node').on('click', function (e) {
	$('#selectable-output').empty();
});

// Free search in Elasticsearch
$('#input-free-search').keypress(function (e) {
	if(e.which == 13){
		e.preventDefault();
		var search_query = $('#input-free-search').val();

		sendVarsToBackend(search_query, function(result){
	  		$('#output-free-search').html(result);
			console.log(result);
		});
	}
});

});
