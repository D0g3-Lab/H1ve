CTFd._internal.challenge.data = undefined;

CTFd._internal.challenge.renderer = CTFd.lib.markdown();

CTFd._internal.challenge.preRender = function () { };

CTFd._internal.challenge.render = function (markdown) {
    return CTFd._internal.challenge.renderer.render(markdown);
};


CTFd._internal.challenge.postRender = function () {
    loadInfo();
};

function stopShowAuto () {
    // 窗口关闭时停止循环
    $("#challenge-window").on("hide.bs.modal", function(event) {
        clearInterval(CTFd._internal.t);
        CTFd._internal.t = undefined;
    });
}

function loadInfo () {
    var challenge_id = parseInt($('#challenge-id').val());
    var url = "/plugins/ctfd-owl/container?challenge_id=" + challenge_id;

    var params = {
    };

    CTFd.fetch(url, {
        method: 'GET',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    }).then(function (response) {
        if (response.status === 429) {
            // User was ratelimited but process response
            return response.json();
        }
        if (response.status === 403) {
            // User is not logged in or CTF is paused.
            return response.json();
        }
        return response.json();
    }).then(function (response) {
        console.log(response);
        if (response.success === false) {
            $('#owl-panel').html(
                    '<h5 class="card-title">Error</h5>' +
                    '<h6 class="card-subtitle mb-2 text-muted" id="owl-challenge-count-down">' + response.msg + '</h6>'
            );
        }
        else if(response.remaining_time === undefined) {
            $('#owl-panel').html(
                    '<h5 class="card-title">Instance Info</h5>' +
                    '<button type="button" class="btn btn-sm btn-outline-secondary" id="owl-button-boot" onclick="CTFd._internal.challenge.boot()">Launch an instance</button>'
            );
        } else {
            if(response.type === 'http') {
                $('#owl-panel').html(
                    '<h5 class="card-title">Instance Info</h5>' +
                    '<h6 class="card-subtitle mb-2 text-muted" id="owl-challenge-count-down">Remaining Time: ' + response.remaining_time + 's</h6>' +
                    '<p class="card-text">http://' + response.domain + '</p>' +
                    '<button type="button" class="btn btn-sm btn-outline-secondary card-link" id="owl-button-destroy" onclick="CTFd._internal.challenge.destroy()">Destroy this instance</button>' +
                    '<button type="button" class="btn btn-sm btn-outline-secondary card-link" onclick="CTFd._internal.challenge.renew()">Renew this instance</button>'
                );
            } else {
                $('#owl-panel').html(
                    '<h5 class="card-title">Instance Info</h5>' +
                    '<h6 class="card-subtitle mb-2 text-muted" id="owl-challenge-count-down">Remaining Time: ' + response.remaining_time + 's</h6>' +
                    '<p class="card-text">' + response.ip + ':' + response.port + '</p>' +
                    '<button type="button" class="btn btn-sm btn-outline-secondary card-link" id="owl-button-destroy" onclick="CTFd._internal.challenge.destroy()">Destroy this instance</button>' +
                    '<button type="button" class="btn btn-sm btn-outline-secondary card-link" id="owl-button-renew" onclick="CTFd._internal.challenge.renew()">Renew this instance</button>'
                );
            }

            if(CTFd._internal.t !== undefined) {
                clearInterval(CTFd._internal.t);
                CTFd._internal.t = undefined;
            }


            function showAuto(){
                const origin = $('#owl-challenge-count-down')[0].innerHTML;
                const second = parseInt(origin.split(": ")[1].split('s')[0]) - 1;
                $('#owl-challenge-count-down')[0].innerHTML = 'Remaining Time: ' + second + 's';
                if(second < 0) {
                    loadInfo();
                }
            }
            CTFd._internal.t = setInterval(showAuto, 1000);
        }
    });
};

CTFd._internal.challenge.destroy = function() {
    var ezal = CTFd.ui.ezq;
    var challenge_id = parseInt($('#challenge-id').val());
    var url = "/plugins/ctfd-owl/container?challenge_id=" + challenge_id;

    $('#owl-button-destroy')[0].innerHTML = "Waiting...";
    $('#owl-button-destroy')[0].disabled = true;

    var params = {
    };

    CTFd.fetch(url, {
        method: 'DELETE',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    }).then(function (response) {
        if (response.status === 429) {
            // User was ratelimited but process response
            return response.json();
        }
        if (response.status === 403) {
            // User is not logged in or CTF is paused.
            return response.json();
        }
        return response.json();
    }).then(function (response) {
        if(response.success) {
            loadInfo();
            ezal.ezAlert({
                title: "Success",
                body: "Your instance has been destroyed!",
                button: "OK"
            });
            stopShowAuto();
        } else {
            $('#owl-button-destroy')[0].innerHTML = "Destroy this instance";
            $('#owl-button-destroy')[0].disabled = false;
            ezal.ezAlert({
                title: "Fail",
                body: response.msg,
                button: "OK"
            });
        }
    });
};

CTFd._internal.challenge.renew = function() {
    var ezal = CTFd.ui.ezq;
    var challenge_id = parseInt($('#challenge-id').val());
    var url = "/plugins/ctfd-owl/container?challenge_id=" + challenge_id;

    $('#owl-button-renew')[0].innerHTML = "Waiting...";
    $('#owl-button-renew')[0].disabled = true;

    var params = {
    };

    CTFd.fetch(url, {
        method: 'PATCH',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    }).then(function (response) {
        if (response.status === 429) {
            // User was ratelimited but process response
            return response.json();
        }
        if (response.status === 403) {
            // User is not logged in or CTF is paused.
            return response.json();
        }
        return response.json();
    }).then(function (response) {
        if(response.success) {
            loadInfo();
            ezal.ezAlert({
                title: "Success",
                body: "Your instance has been renewed!",
                button: "OK"
            });
        } else {
            $('#owl-button-renew')[0].innerHTML = "Renew this instance";
            $('#owl-button-renew')[0].disabled = false;
            ezal.ezAlert({
                title: "Fail",
                body: response.msg,
                button: "OK"
            });
        }
    });
};

CTFd._internal.challenge.boot = function () {
    var ezal = CTFd.ui.ezq;
    var challenge_id = parseInt($('#challenge-id').val());
    var url = "/plugins/ctfd-owl/container?challenge_id=" + challenge_id;

    $('#owl-button-boot')[0].innerHTML = "Waiting...";
    $('#owl-button-boot')[0].disabled = true;

    var params = {
    };

    CTFd.fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    }).then(function (response) {
        if (response.status === 429) {
            // User was ratelimited but process response
            return response.json();
        }
        if (response.status === 403) {
            // User is not logged in or CTF is paused.
            return response.json();
        }
        return response.json();
    }).then(function (response) {
        if(response.success) {
            loadInfo();
            ezal.ezAlert({
                title: "Success",
                body: "Your instance has been deployed!",
                button: "OK"
            });
        } else {
            $('#owl-button-boot')[0].innerHTML = "Launch an instance";
            $('#owl-button-boot')[0].disabled = false;
            ezal.ezAlert({
                title: "Fail",
                body: response.msg,
                button: "OK"
            });
        }
    });
};


CTFd._internal.challenge.submit = function (cb, preview) {
    var ezal = CTFd.ui.ezq;
    var challenge_id = parseInt($('#challenge-id').val());
    var submission = $('#submission-input').val();
    var url = "/api/v1/challenges/attempt";

    if (preview) {
        url += "?preview=true";
    }

    var params = {
        'challenge_id': challenge_id,
        'submission': submission
    };

    CTFd.fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    }).then(function (response) {
        if (response.status === 429) {
            // User was ratelimited but process response
            return response.json();
        }
        if (response.status === 403) {
            // User is not logged in or CTF is paused.
            return response.json();
        }
        return response.json();
    }).then(function (response) {
        cb(response);
    });
};

CTFd._internal.challenge.start = function (cb, preview) {
    var challenge_id = parseInt($('#challenge-id').val());
    var url = "/api/v1/challenges/start";



    var params = {
        'challenge_id': challenge_id,
    };

    CTFd.fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    }).then(function (response) {
        if (response.status === 429) {
            // User was ratelimited but process response
            return response.json();
        }
        if (response.status === 403) {
            // User is not logged in or CTF is paused.
            return response.json();
        }
        return response.json();
    }).then(function (response) {
        cb(response);
    });
};

CTFd._internal.challenge.delete = function (cb, preview) {
    var challenge_id = parseInt($('#challenge-id').val());
    var url = "/api/v1/challenges/delete";

    

    var params = {
        'challenge_id': challenge_id,
    };

    CTFd.fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    }).then(function (response) {
        if (response.status === 429) {
            // User was ratelimited but process response
            return response.json();
        }
        if (response.status === 403) {
            // User is not logged in or CTF is paused.
            return response.json();
        }
        return response.json();
    }).then(function (response) {
        cb(response);
    });
};