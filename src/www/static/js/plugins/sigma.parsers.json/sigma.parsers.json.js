;(function (undefined) {
    'use strict';

    if (typeof sigma === 'undefined')
        throw 'sigma is not declared';

    // Initialize package:
    sigma.utils.pkg('sigma.parsers');
    sigma.utils.pkg('sigma.utils');

    /**
     * Just an XmlHttpRequest polyfill for different IE versions.
     *
     * @return {*} The XHR like object.
     */
    sigma.utils.xhr = function () {
        if (window.XMLHttpRequest)
            return new XMLHttpRequest();

        var names,
            i;

        if (window.ActiveXObject) {
            names = [
                'Msxml2.XMLHTTP.6.0',
                'Msxml2.XMLHTTP.3.0',
                'Msxml2.XMLHTTP',
                'Microsoft.XMLHTTP'
            ];

            for (i in names)
                try {
                    return new ActiveXObject(names[i]);
                } catch (e) {
                }
        }

        return null;
    };

    /**
     * This function loads a JSON file and creates a new sigma instance or
     * updates the graph of a given instance. It is possible to give a callback
     * that will be executed at the end of the process.
     *
     * @param  {string}       url      The URL of the JSON file.
     * @param  {object|sigma} sig      A sigma configuration object or a sigma
     *                                 instance.
     * @param  {?function}    callback Eventually a callback to execute after
     *                                 having parsed the file. It will be called
     *                                 with the related sigma instance as
     *                                 parameter.
     */
    sigma.parsers.json = function (url, sig, callback) {
        var graph,
            xhr = sigma.utils.xhr();

        if (!xhr)
            throw 'XMLHttpRequest not supported, cannot load the file.';

        xhr.open('GET', url, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                var data = xhr.responseText;
                data = data.replace("links", "edges")
                graph = JSON.parse(data);
                var i = 0;
                var j = 0;


                var MIN = graph.nodes.reduce(function (prev, curr) {
                    return prev.size < curr.size ? prev : curr;
                });
                var MAX = graph.nodes.reduce(function (prev, curr) {
                    return prev.size > curr.size ? prev : curr;
                });
                var maxvalue = MAX.size;




                debugger;

                var paletteScale = d3.scale.log()
                    .domain([MIN.size, MAX.size])
                    .range(["#000000", "#c62540"]);

                for (i in graph.nodes) {
                    var node = graph.nodes[i];
                    node.id = (parseFloat(node.id)).toFixed(1).toString()
                    node["info"] = node.label;
                    node.label = parseInt(node.id).toString() + " - (" + node.size + ")";

                    var colour = paletteScale(node.size)
                    node.size = parseInt((node.size / maxvalue) * 16) + 4

                    node["color"] = colour
                }

                for (j in graph.edges) {
                    var edges = graph.edges[j];
                    edges.id = (parseFloat(j)).toFixed(1).toString()
                    edges.source = (parseFloat(edges.source)).toFixed(1).toString()
                    edges.target = (parseFloat(edges.target)).toFixed(1).toString()
                    edges["size"] = 1
                    edges["color"] = 'rgba(198, 36, 63, 0.5)'

                }

                debugger;

                // Update the instance's graph:
                if (sig instanceof sigma) {
                    sig.graph.clear();
                    sig.graph.read(graph);

                    // ...or instantiate sigma if needed:
                } else if (typeof sig === 'object') {
                    sig.graph = graph;
                    sig = new sigma(sig);


                    // ...or it's finally the callback:
                } else if (typeof sig === 'function') {
                    callback = sig;
                    sig = null;
                }

                // Call the callback if specified:
                if (callback)
                    callback(sig || graph);
            }
        };
        xhr.send();
    };
}).call(this);
