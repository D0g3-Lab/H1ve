"use strict";"object"!=typeof window.CP&&(window.CP={}),window.CP.PenTimer={programNoLongerBeingMonitored:!1,timeOfFirstCallToShouldStopLoop:0,_loopExits:{},_loopTimers:{},START_MONITORING_AFTER:2e3,STOP_ALL_MONITORING_TIMEOUT:5e3,MAX_TIME_IN_LOOP_WO_EXIT:2200,exitedLoop:function(o){this._loopExits[o]=!0},shouldStopLoop:function(o){if(this.programKilledSoStopMonitoring)return!0;if(this.programNoLongerBeingMonitored)return!1;if(this._loopExits[o])return!1;var t=this._getTime();if(0===this.timeOfFirstCallToShouldStopLoop)return this.timeOfFirstCallToShouldStopLoop=t,!1;var i=t-this.timeOfFirstCallToShouldStopLoop;if(i<this.START_MONITORING_AFTER)return!1;if(i>this.STOP_ALL_MONITORING_TIMEOUT)return this.programNoLongerBeingMonitored=!0,!1;try{this._checkOnInfiniteLoop(o,t)}catch(n){return this._sendErrorMessageToEditor(),this.programKilledSoStopMonitoring=!0,!0}return!1},_sendErrorMessageToEditor:function(){try{if(this._shouldPostMessage()){var o={action:"infinite-loop",line:this._findAroundLineNumber()};parent.postMessage(JSON.stringify(o),"*")}else this._throwAnErrorToStopPen()}catch(t){this._throwAnErrorToStopPen()}},_shouldPostMessage:function(){return document.location.href.match(/boomerang/)},_throwAnErrorToStopPen:function(){throw"We found an infinite loop in your Pen. We've stopped the Pen from running. Please correct it or contact support@codepen.io."},_findAroundLineNumber:function(){var o=new Error,t=0;if(o.stack){var i=o.stack.match(/boomerang\S+:(\d+):\d+/);i&&(t=i[1])}return t},_checkOnInfiniteLoop:function(o,t){if(!this._loopTimers[o])return this._loopTimers[o]=t,!1;var i=t-this._loopTimers[o];if(i>this.MAX_TIME_IN_LOOP_WO_EXIT)throw"Infinite Loop found on loop: "+o},_getTime:function(){return+new Date}},window.CP.shouldStopExecution=function(o){return window.CP.PenTimer.shouldStopLoop(o)},window.CP.exitedLoop=function(o){window.CP.PenTimer.exitedLoop(o)};
(function ($) {
    $.fn.jaliswall = function (options) {
        this.each(function () {
            var defaults = {
                item: '.wall-item',
                columnClass: '.wall-column',
                resize: true
            };
            var prm = $.extend(defaults, options);
            var container = $(this);
            var items = container.find(prm.item);
            var elemsDatas = [];
            var columns = [];
            var nbCols = getNbCols();
            init();
            function init() {
                nbCols = getNbCols();
                recordAndRemove();
                print();
                if (prm.resize) {
                    $(window).resize(function () {
                        if (nbCols != getNbCols()) {
                            nbCols = getNbCols();
                            setColPos();
                            print();
                        }
                    });
                }
            }
            function getNbCols() {
                var instanceForCompute = false;
                if (container.find(prm.columnClass).length == 0) {
                    instanceForCompute = true;
                    container.append('<div class=\'' + parseSelector(prm.columnClass) + '\'></div>');
                }
                var colWidth = container.find(prm.columnClass).outerWidth(true);
                var wallWidth = container.innerWidth();
                if (instanceForCompute)
                    container.find(prm.columnClass).remove();
                return Math.round(wallWidth / colWidth);
            }
            function recordAndRemove() {
                items.each(function (index) {
                    var item = $(this);
                    elemsDatas.push({
                        content: item.html(),
                        class: item.attr('class'),
                        href: item.attr('href'),
                        id: item.attr('id'),
                        colid: index % nbCols
                    });
                    item.remove();
                });
            }
            function setColPos() {
                for (var i in elemsDatas) {
                    if (window.CP.shouldStopExecution(1)) {
                        break;
                    }
                    elemsDatas[i].colid = i % nbCols;
                }
                window.CP.exitedLoop(1);
            }
            function parseSelector(selector) {
                return selector.slice(1, selector.length);
            }
            function print() {
                var tree = '';
                for (var i = 0; i < nbCols; i++) {
                    if (window.CP.shouldStopExecution(2)) {
                        break;
                    }
                    tree += '<div class=\'' + parseSelector(prm.columnClass) + '\'></div>';
                }
                window.CP.exitedLoop(2);
                container.html(tree);
                for (var i in elemsDatas) {
                    var html = '';
                    var content = elemsDatas[i].content != undefined ? elemsDatas[i].content : '';
                    var href = elemsDatas[i].href != href ? elemsDatas[i].href : '';
                    var classe = elemsDatas[i].class != undefined ? elemsDatas[i].class : '';
                    var id = elemsDatas[i].id != undefined ? elemsDatas[i].id : '';
                    if (elemsDatas[i].href != undefined) {
                        html += '<a ' + getAttr(href, 'href') + ' ' + getAttr(classe, 'class') + ' ' + getAttr(id, 'id') + '>' + content + '</a>';
                    } else {
                        html += '<div ' + getAttr(classe, 'class') + ' ' + getAttr(id, 'id') + '>' + content + '</a>';
                    }
                    container.children(prm.columnClass).eq(i % nbCols).append(html);
                }
            }
            function getAttr(attr, type) {
                return attr != undefined ? type + '=\'' + attr + '\'' : '';
            }
        });
        return this;
    };
	
}(jQuery));