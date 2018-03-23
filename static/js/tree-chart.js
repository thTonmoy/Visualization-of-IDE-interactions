function tree() {
    var data,
        i = 0,
        duration = 750,
        margin = {top: 20, right: 10, bottom: 30, left: 30},
	    width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom,
        update;

    function chart(selection){
        selection.each(function() {
        	height = height - margin.top - margin.bottom;
        	width = width - margin.left - margin.right;
            // append the svg object to the selection
            var svg = selection.append('svg')
                .attr('width', width + margin.left + margin.right)
                .attr('height', height + margin.top + margin.bottom)
              .append('g')
                .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

            // declares a tree layout and assigns the size of the tree
            var treemap = d3.tree().size([height, width]);

            // assign parent, children, height, depth
            var root = d3.hierarchy(data, function(d) { return d.children });
            root.x0 = height / 2; // left edge of the rectangle
            root.y0 = 0; // top edge of the triangle

	        // collapse after the second level
	        root.children.forEach(collapse);

	        update(root);

	        // collapse the node and all it's children
	        function collapse(d) {
	        	if (d.children) {
	        		d._children = d.children;
	        		d._children.forEach(collapse);
			        d.children = null;
		        }
	        }

	        function update(source) {

	        	// assigns the x and y position for the nodes
		        var treeData = treemap(root);

		        // compute the new tree layout
		        var nodes = treeData.descendants(),
		            links = treeData.descendants().slice(1);

		        // normalise for fixed depth
		        nodes.forEach(function(d) { d.y = d.depth * 180; });

		        // ****************** Nodes section ***************************

		        // update the nodes ...
		        var node = svg.selectAll('g.node')
			        .data(nodes, function(d) { return d.id || (d.id = ++i); });

		        // Enter any new modes at the parent's previous position.
		        var nodeEnter = node.enter().append('g')
			        .attr('class', 'node')
			        .attr('transform', function(d) {
			        	return 'translate(' + (source.y0 + margin.top) + ',' + (source.x0 + margin.left) + ')';
			        })
			        .on('click', click);

		        // add circle for the nodes
		        nodeEnter.append('circle')
			        .attr('class', 'node')
			        .attr('r', 1e-6)
			        .style('fill', function(d) {
			        	return d._children ? 'lightsteelblue' : '#fff';
			        });

		        // add labels for the nodes
		        nodeEnter.append('text')
			        .attr('dy', '.35em')
			        .attr('x', function(d) {
			        	return d.children || d._children ? 0 : 13;
			        })
			        .attr('y', function(d) {
			        	return d.children || d._children ? -margin.top : 0;
			        })
			        .attr('text-anchor', function(d) {
			        	return d.children || d._children ? 'middle' : 'start';
			        })
			        .text(function(d) {
			        	return (d.children || d._children) ? d.data.id.capitalize() : d.data.id;
			        });

		        // add number of children to node circle
		        nodeEnter.append('text')
			        .attr('x', -3)
			        .attr('y', 3)
			        .attr('cursor', 'pointer')
			        .style('font-size', '10px')
			        .text(function(d) {
			        	if (d.children) return d.children.length;
			        	else if (d._children) return d._children.length;
			        });

		        // UPDATE
		        var nodeUpdate = nodeEnter.merge(node);

		        // transition to the proper position for the node
		        nodeUpdate.transition().duration(duration)
			        .attr('transform', function(d) {
			        	return 'translate(' + (d.y + margin.top) + ',' + (d.x + margin.left) + ')';
			        });

		        // update the node attributes and style
		        nodeUpdate.select('circle.node')
			        .attr('r', 9)
			        .style('fill', function(d) {
			        	return d._children ? 'lightsteelblue' : '#fff';
			        })
			        .attr('cursor', 'pointer');

		        // remove any exiting nodes
		        var nodeExit = node.exit()
			        .transition().duration(duration)
			        .attr('transform', function(d) {
			        	return 'translate(' + (source.y + margin.top) + ',' + (source.x + margin.left) + ')';
			        })
			        .remove();

		        // on exit reduce the node circles size to 0
		        nodeExit.select('circle')
			        .attr('r', 1e-6);

		        // on exit reduce the opacity of text labels
		        nodeExit.select('text')
			        .style('fill-opacity', 1e-6);

		        // ****************** links section ***************************

		        // update the links
		        var link = svg.selectAll('path.link')
			        .data(links, function(d) { return d.id });

		        // enter any new links at the parent's previous position
		        var linkEnter = link.enter().insert('path', 'g')
			        .attr('class', 'link')
			        .attr('d', function(d) {
			        	var o = {x: source.x0 + margin.left, y: source.y0 + margin.top};
			        	return diagonal(o, o);
			        });

		        // UPDATE
		        var linkUpdate = linkEnter.merge(link);

		        // transition back to the parent element position
		        linkUpdate.transition().duration(duration)
			        .attr('d', function(d) { return diagonal(d, d.parent); });

		        // remove any exiting links
		        var linkExit = link.exit()
			        .transition().duration(duration)
			        .attr('d', function(d) {
			        	var o = {x: source.x, y: source.y};
			        	return diagonal(o, o);
			        })
			        .remove();

		        // store the old positions for transition
		        nodes.forEach(function(d) {
		        	d.x0 = d.x + margin.left;
		        	d.y0 = d.y + margin.top;
		        });

		        // creates a curved (diagonal) path from parent to the child nodes
		        function diagonal(s, d) {
		        	path = 'M ' + (s.y + margin.top) + ' ' + (s.x + margin.left) +
					        'C ' + ((s.y + d.y + (margin.top * 2)) / 2) + ' ' + (s.x + margin.left) +
					        ', ' + ((s.y + d.y + (margin.top * 2)) / 2) + ' ' + (d.x + margin.left) +
					        ', ' + (d.y + margin.top) + ' ' + (d.x + margin.left);
		        	return path;
		        }

		        // toggle children on click
		        function click(d) {
		        	if (d.children) {
		        		d._children = d.children;
		        		d.children = null;
			        } else {
		        		d.children = d._children;
		        		d._children = null;
			        }
			        update(d);
		        }

	        }
        });
    }

    chart.width = function(value) {
        if (!arguments.length) return width;
        width = value;
        return chart;
    };

    chart.height = function(value) {
        if (!arguments.length) return height;
        height = value;
        return chart;
    };

    chart.margin = function(value) {
        if (!arguments.length) return margin;
        margin = value;
        return chart;
    };

	chart.data = function(value) {
		if (!arguments.length) return data;
		data = value;
		if (typeof updateData === 'function') updateData();
		return chart;
	};

	String.prototype.capitalize = function() {
		return this.charAt(0).toUpperCase() + this.slice(1).toLowerCase();
	};

    return chart;
}