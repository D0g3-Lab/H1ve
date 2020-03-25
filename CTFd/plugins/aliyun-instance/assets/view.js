window.challenge.data = undefined;

window.challenge.renderer = new markdownit({
    html: true,
    linkify: true,
});

window.challenge.preRender = function () {

};

window.challenge.render = function (markdown) {
    return window.challenge.renderer.render(markdown);
};


window.challenge.postRender = function () {
    loadInfo();
};

function stopShowAuto () {
    // 窗口关闭时停止循环
    $("#challenge-window").on("hide.bs.modal", function(event) {
        clearInterval(window.t);
        window.t = undefined;
    });
}

function loadInfo () {
    var challenge_id = parseInt($('#challenge-id').val());
    var url = "/plugins/aliyun-instance/container?challenge_id=" + challenge_id;

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
            $('#ali-ecs-panel').html(
                    '<h5 class="card-title">Error</h5>' +
                    '<h6 class="card-subtitle mb-2 text-muted" id="ali-ecs-challenge-count-down">' + response.msg + '</h6>'
            );
        }
        else if(response.remaining_time === undefined) {
            $('#ali-ecs-panel').html(
                    '<h5 class="card-title">Instance Info</h5>' +
                    '<button type="button" class="btn btn-primary card-link" id="ali-ecs-button-boot" onclick="window.challenge.boot()">Launch an instance</button>'
            );
        } else {

            $('#ali-ecs-panel').html(
                '<h5 class="card-title">Instance Info</h5>' +
                '<h6 class="card-subtitle mb-2 text-muted" id="ali-ecs-challenge-count-down">Remaining Time: ' + response.remaining_time + 's</h6>' +
                '<p class="card-text">' + response.ip +  '</p>' +
                '<button type="button" class="btn btn-sm btn-outline-secondary" id="ali-ecs-button-destroy" onclick="window.challenge.destroy()">Destroy this instance</button>' +
                '<button type="button" class="btn btn-sm btn-outline-secondary" id="ali-ecs-button-renew" onclick="window.challenge.renew()">Renew this instance</button>'
            );

            if(window.t !== undefined) {
                clearInterval(window.t);
                window.t = undefined;
            }


            function showAuto(){
                const origin = $('#ali-ecs-challenge-count-down')[0].innerHTML;
                const second = parseInt(origin.split(": ")[1].split('s')[0]) - 1;
                $('#ali-ecs-challenge-count-down')[0].innerHTML = 'Remaining Time: ' + second + 's';
                if(second < 0) {
                    loadInfo();
                }
            }
            window.t = setInterval(showAuto, 1000);
        }
    });
};

window.challenge.destroy = function() {
    var challenge_id = parseInt($('#challenge-id').val());
    var url = "/plugins/aliyun-instance/container?challenge_id=" + challenge_id;

    $('#ali-ecs-button-destroy')[0].innerHTML = "Waiting...";
    $('#ali-ecs-button-destroy')[0].disabled = true;

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
            ezal({
                title: "Success",
                body: "Your instance has been destroyed!",
                button: "OK"
            });
            stopShowAuto();
        } else {
            $('#ali-ecs-button-destroy')[0].innerHTML = "Destroy this instance";
            $('#ali-ecs-button-destroy')[0].disabled = false;
            ezal({
                title: "Fail",
                body: response.msg,
                button: "OK"
            });
        }
    });
};

window.challenge.renew = function() {
    var challenge_id = parseInt($('#challenge-id').val());
    var url = "/plugins/aliyun-instance/container?challenge_id=" + challenge_id;

    $('#ali-ecs-button-renew')[0].innerHTML = "Waiting...";
    $('#ali-ecs-button-renew')[0].disabled = true;

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
            ezal({
                title: "Success",
                body: "Your instance has been renewed!",
                button: "OK"
            });
        } else {
            $('#ali-ecs-button-renew')[0].innerHTML = "Renew this instance";
            $('#ali-ecs-button-renew')[0].disabled = false;
            ezal({
                title: "Fail",
                body: response.msg,
                button: "OK"
            });
        }
    });
};

window.challenge.boot = function () {
    var challenge_id = parseInt($('#challenge-id').val());
    var url = "/plugins/aliyun-instance/container?challenge_id=" + challenge_id;

    $('#ali-ecs-button-boot')[0].innerHTML = "Waiting...";
    $('#ali-ecs-button-boot')[0].disabled = true;

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
            ezal({
                title: "Success",
                body: "Your instance has been deployed!",
                button: "OK"
            });
        } else {
            $('#ali-ecs-button-boot')[0].innerHTML = "Launch an instance";
            $('#ali-ecs-button-boot')[0].disabled = false;
            ezal({
                title: "Fail",
                body: response.msg,
                button: "OK"
            });
        }
    });
};


window.challenge.submit = function (cb, preview) {
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

window.challenge.start = function (cb, preview) {
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

window.challenge.delete = function (cb, preview) {
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