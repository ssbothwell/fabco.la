document.addEventListener("DOMContentLoaded", function() {

  var tbody = document.getElementById('lineitems');
  var rows = tbody.children.length;
  //alert(rows);
  //for ( var i = 0; i < rows; i++ ) {
    //alert(tbody.children[0].children.value);
  //}
});


function deleteFunction(el) {
    // Get form field IDs
    var row = el.parentNode.parentNode.id;
    var checkbox = 'id_' + row.slice(0, -3) + 'DELETE';
    var description = 'id_' + row.slice(0, -3) + 'description';
    var price = 'id_' + row.slice(0, -3) + 'price';
    var quantity = 'id_' + row.slice(0, -3) + 'quantity';

    // Check hidden delete checkbox
    if(document.getElementById(checkbox)) {
        document.getElementById(checkbox).checked = true;
    };
    // Clear form fields
    document.getElementById(description).value = '';
    document.getElementById(price).value = '';
    document.getElementById(quantity).value = '';
    // Hide row
    document.getElementById(row).style.display = 'none';
};
function lineItemSelector(selection) {

    // LineItem Table Row
    var tableRow = document.createElement("tr");
    var lineItemCount = document.querySelectorAll('#lineitems tr').length;
    tableRow.setAttribute('id','line_item-'+lineItemCount+'-row');

    // Columns
    var orderColumn = document.createElement("td");
    var descriptionColumn = document.createElement("td");
    var unitCostColumn = document.createElement("td");
    var quantityColumn = document.createElement("td");
    var taxableColumn = document.createElement("td");
    var deleteColumn = document.createElement("td");

    //// Fields:

    // ID

    var idField = document.createElement("input");
    idField.setAttribute("id", "id_line_item-"+lineItemCount+'-id');
    idField.setAttribute("name", "line_item-"+lineItemCount+'-id');
    idField.setAttribute("type", "hidden");

    // Order
    var orderSpan = document.createElement("span");
    orderSpan.setAttribute("class","glyphicon glyphicon-sort ui-sortable-handle");
    orderSpan.setAttribute("style", "cursor: move;");

    var orderField = document.createElement("input");
    orderField.setAttribute("id", "id_line_item-"+lineItemCount+"-order");
    orderField.setAttribute("name", "line_item-"+lineItemCount+"-order");
    orderField.setAttribute("type", "number");
    orderField.setAttribute("value", lineItemCount);

    // Name (hidden)
    var nameLabel = document.createElement("label");
    var labelText = document.createTextNode(selection.value);

    nameLabel.setAttribute("value", selection.value);
    nameLabel.setAttribute("for", "name");
    nameLabel.appendChild(labelText);

    var nameField = document.createElement("input");
    nameField.setAttribute("value", selection.value);
    nameField.setAttribute("id", "id_line_item-"+lineItemCount+"-name");
    nameField.setAttribute("name", "line_item-"+lineItemCount+"-name");
    nameField.setAttribute("type", "hidden");

    // Description
    var descriptionField = document.createElement("textarea");
    descriptionField.setAttribute("class", "form-control")
    descriptionField.setAttribute("id", "id_line_item-"+lineItemCount+"-description");
    descriptionField.setAttribute("type", "text");
    descriptionField.setAttribute("name", "line_item-"+lineItemCount+"-description");
    descriptionField.setAttribute("maxLength", "200");
    descriptionField.setAttribute("cols", "40");
    descriptionField.setAttribute("rows","2");

    // Price
    var unitCostField = document.createElement("input");
    unitCostField.setAttribute("class", "form-control");
    unitCostField.setAttribute("id", "id_line_item-"+lineItemCount+"-price");
    unitCostField.setAttribute("name", "line_item-"+lineItemCount+"-price");
    unitCostField.setAttribute("type", "text");
    unitCostField.setAttribute("size", "10");

    // Quantity
    var quantityField = document.createElement("input");
    quantityField.setAttribute("class", "form-control");
    quantityField.setAttribute("id", "id_line_item-"+lineItemCount+"-quantity");
    quantityField.setAttribute("name", "line_item-"+lineItemCount+"-quantity");
    quantityField.setAttribute("type", "text");
    quantityField.setAttribute("size", "10");

    // Taxable
    var taxableField = document.createElement("input");
    taxableField.setAttribute("class", "form-control");
    taxableField.setAttribute("id", "id_line_item-"+lineItemCount+"-taxable");
    taxableField.setAttribute("name", "line_item-"+lineItemCount+"-taxable");
    taxableField.setAttribute("type", "checkbox");

    // Delete
    var deleteIcon = document.createElement("a");
    deleteIcon.setAttribute("class", "glyphicon glyphicon-trash");
    deleteIcon.setAttribute("href", "javascript:void(0)");
    deleteIcon.setAttribute("onClick", "deleteFunction(this)");

    var deleteField = document.createElement("input");
    deleteField.setAttribute("class", "form-control");
    deleteField.setAttribute("type", "checkbox");
    //deleteField.setAttribute("style", "display:none");
    // Pack DOM

    //orderColumn
    orderSpan.appendChild(orderField);
    orderColumn.appendChild(orderSpan);
    descriptionColumn.appendChild(deleteField);
    descriptionColumn.appendChild(nameLabel);
    descriptionColumn.appendChild(nameField);
    descriptionColumn.appendChild(descriptionField);
    unitCostColumn.appendChild(unitCostField);
    quantityColumn.appendChild(quantityField);
    taxableColumn.appendChild(taxableField);
    deleteColumn.appendChild(deleteIcon);

    tableRow.appendChild(idField);
    tableRow.appendChild(orderColumn);
    tableRow.appendChild(descriptionColumn);
    tableRow.appendChild(unitCostColumn);
    tableRow.appendChild(quantityColumn);
    tableRow.appendChild(taxableColumn);
    tableRow.appendChild(deleteColumn);

    document.getElementById('lineitems').appendChild(tableRow);

    document.getElementById('id_LineItemType').selectedIndex = 0;

    // update  total forms
    //$('#id_line_item-TOTAL_FORMS').attr('value', count+1);
    document.getElementById('id_line_item-TOTAL_FORMS').value = lineItemCount + 1;
};
