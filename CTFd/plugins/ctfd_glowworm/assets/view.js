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
    get_targets($("#challenge-id").val());
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
    var url = "/plugins/ctfd-glowworm/container?challenge_id=" + challenge_id;

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
        if(response.service_port === undefined) {
            $('#glowworm-panel').html(
                    '<h5 class="card-title">Instance Info</h5>' +
                    '<h6 class="card-subtitle mb-2 text-muted"> Instance not started.</h6>'
            );
        } else {
            if(response.type === 'http') {
                $('#glowworm-panel').html(
                    '<h5 class="card-title">Instance Info</h5>' +
                    // '<h6 class="card-subtitle mb-2 text-muted" id="owl-challenge-count-down">Remaining Time: ' + response.remaining_time + 's</h6>' +
                    '<p class="card-text">http://' + response.domain + '</p>' +
                    '<button type="button" class="btn btn-sm btn-outline-secondary" id="glowworm-button-renew" onclick="window.challenge.renew()">Renew this instance</button>'
                );
            } else {
                $('#glowworm-panel').html(
                    '<h5 class="card-title">Instance Info</h5>' +
                    // '<h6 class="card-subtitle mb-2 text-muted" id="owl-challenge-count-down">Remaining Time: ' + response.remaining_time + 's</h6>' +
                    '<p class="card-text">' + response.ip + '<br>SSH Port: ' + response.ssh_port + '<br>Service Port: ' + response.service_port + '</p>' +
                    '<p class="card-text">SSH Key:<br>web/pwn:' + response.ssh_key + '</p>' +
                    // '<button type="button" class="btn btn-sm btn-outline-secondary" id="glowworm-button-destroy" onclick="window.challenge.destroy()">Destroy this instance</button>' +
                    '<button type="button" class="btn btn-sm btn-outline-secondary" id="glowworm-button-renew" onclick="window.challenge.renew()">Renew this instance</button>'
                );
            }

            if(window.t !== undefined) {
                clearInterval(window.t);
                window.t = undefined;
            }


            // function showAuto(){
            //     const origin = $('#owl-challenge-count-down')[0].innerHTML;
            //     const second = parseInt(origin.split(": ")[1].split('s')[0]) - 1;
            //     $('#owl-challenge-count-down')[0].innerHTML = 'Remaining Time: ' + second + 's';
            //     if(second < 0) {
            //         loadInfo();
            //     }
            // }
            // window.t = setInterval(showAuto, 1000);
        }
    });
};

window.challenge.renew = function() {
    var challenge_id = parseInt($('#challenge-id').val());
    var url = "/plugins/ctfd-glowworm/container?challenge_id=" + challenge_id;

    $('#glowworm-button-renew')[0].innerHTML = "Waiting...";
    $('#glowworm-button-renew')[0].disabled = true;

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
            $('#glowworm-button-renew')[0].innerHTML = "Renew this instance";
            $('#glowworm-button-renew')[0].disabled = false;
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

function get_targets(id) {
  $.get(script_root + "/plugins/ctfd-glowworm/challenge/" + id, function(
    response
  ) {
    var data = response.data;
    $(".challenge-targets").text(parseInt(data.length) + " Targets");
    var box = $("#challenge-targets-lists");
    box.empty();
    for (var i = 0; i < data.length; i++) {
      var target = data[i].target;
      box.append(
        '<tr><td>{0}</td></tr>'.format(
          htmlentities(target),
        )
      );
    }
  });
}

$("#targets").click(function(e) {
  get_targets($("#challenge-id").val());
});
