function getParameterByName(name, url) {
    if (!url) {
        url = window.location.href;
    }
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function loadTweetContainer(tweetContainerID, fetchOneID) {
    var query = getParameterByName('q'),
        tweetList = [],
        nextTweetURL,
        tweetContainer;
    if (tweetContainerID) {
        tweetContainer = $("#" + tweetContainerID)
    } else {
        tweetContainer = $("#tweet-container")
    }

    var initialURL = tweetContainer.attr("data-url") || "/api/tweet/";

    $(document.body).on("click", ".tweet-like", function (e) {
        e.preventDefault();
        var this_ = $(this),
            tweetID = this_.attr("data-id"),
            likedURL = '/api/tweet/' + tweetID + "/like/";
        $.ajax({
            method: "GET",
            url: likedURL,
            success: function (data) {
                if (data.liked) {
                    this_.text("Liked")
                } else {
                    this_.text("Unlike")
                }
            },
            error: function (data) {
                console.log("error");
                console.log(data);
            }

        })
    });

    $(document.body).on("click", ".tweet-reply", function (e) {
        console.log(e);
        e.preventDefault();
        var this_ = $(this),
            parentID = this_.attr("data-id"),
            username = this_.attr("data-user"),
            content = this_.parent().parent().find(".content").text();
        $("#replyModal").modal({});
        $("#replyModal textarea").after("<input type='hidden' value='" + parentID + "' name='parent_id'/>");
        $("#replyModal textarea").after("<input type='hidden' value='" + true + "' name='reply'/>");
        $("#replyModal textarea").val("@" + username + " ");
        $("#replyModal #replyModalLabel").text("Reply to " + content);
        $("#replyModal").on("shown.bs.modal", function () {
            $("textarea").focus()
        });
    });

    $(document.body).on("click", ".retweetBtn", function (e) {
        e.preventDefault();
        var url = "/api" + $(this).attr("href");
        $.ajax({
            method: "GET",
            url: url,
            success: function (data) {
                if (initialURL == "/api/tweet/") {
                    attachTweet(data, true, true);
                    updateHashLinks()
                }
            },
            error: function (data) {
                console.log("error");
                console.log(data);
            }
        })
    });


    function updateHashLinks() {
        $(".content").each(function (data) {
            var hashtagRegex = /(^|\s)#([\w\d-]]+)/g,
                usernameRegex = /(^|\s)@([\w\d-]]+)/g,
                currentHTML = $(this).html(),
                newText;

            newText = currentHTML.replace(hashtagRegex, "$1<a href='/tags/$2/'>#$2</a>");
            newText = newText.replace(hashtagRegex, "$1 @<a href='/$2/'>$2</a>");
            $(this).html(newText)
        })
    }

    function formatTweet(tweetValue) {
        var preContent,
            container,
            tweetContent,
            isReply = tweetValue.reply,
            replyID = tweetValue.id;
        if (tweetValue.parent) {
            replyID = tweetValue.parent.id
        }

        var openingContainerDIV = "<div class='media'>";
        if (tweetValue.id == fetchOneID) {
            openingContainerDIV = "<div class='media media-focus'>";
            setTimeout(function () {
                $(".media-focus").css("background-color", '#fff')
            }, 2000)
        }

        if (tweetValue.parent && !isReply) {
            tweetValue = tweetValue.parent;
            preContent = `<span class='grey-color'>Retweet via ${tweetValue.user.username} on ${tweetValue.date_display}</span><br/>`
        } else if (tweetValue.parent && isReply) {
            preContent = `<span class='grey-color'>Reply to @ ${tweetValue.parent.user.username}</span><br/>`;
        }

        var verb = 'Like';
        if (tweetValue.did_like) {
            verb = "Unlike";
        }

        tweetContent = `<span class='content'>${tweetValue.content}</span><br/>
                    via <a href='${tweetValue.user.url}'>${tweetValue.user.username}</a> | ${tweetValue.date_display} |
                    <a href="/tweet/${tweetValue.id}">View</a> | <a class="retweetBtn" href="/tweet/${tweetValue.id}/retweet/">Retweet</a> | 
                    <a href="#" class="tweet-like" data-id="${tweetValue.id}">${verb} (${tweetValue.likes})</a> |
                    <a href="#" class="tweet-reply" data-user="${tweetValue.user.username}" data-id="${replyID}">Reply</a>`;

        if (preContent) {
            container = `${openingContainerDIV}<div class="media-body">${preContent + tweetContent}</div></div><hr/>`;
        } else {
            container = `${openingContainerDIV}<div class="media-body">${tweetContent}</div></div><hr/>`;
        }


        return container;
    }

    function attachTweet(tweetValue, prepend, retweet) {
        var tweetFormattedHTML = formatTweet(tweetValue);

        if (prepend == true) {
            tweetContainer.prepend(tweetFormattedHTML);
        } else {
            tweetContainer.append(tweetFormattedHTML);
        }
    }

    function parseTweets() {
        if (tweetList == 0) {
            tweetContainer.text("No tweets currently found");
        } else {
            $.each(tweetList, function (key, value) {
                var tweetKey = key;
                if (value.parent) {
                    attachTweet(value, false, true)
                } else {
                    attachTweet(value)
                }
            })
        }
    }

    function fetchTweets(url) {
        var fetchURL;
        if (!url) {
            fetchURL = initialURL;
        } else {
            fetchURL = url;
        }
        $.ajax({
            url: fetchURL,
            data: {
                "q": query
            },
            method: "GET",
            success: function (data) {
                tweetList = data.results
                if (data.next) {
                    nextTweetURL = data.next
                } else {
                    $("#loadmore").css("display", "none")
                }
                parseTweets();
                updateHashLinks();
            },
            error: function (data) {
                console.log("error");
                console.log(data);
            }

        })
    }

    function fetchSingle(fetchOneID) {
        var fetchDetailURL = "/api/tweet/" + fetchOneID;
        $.ajax({
            url: fetchDetailURL,
            method: "GET",
            success: function (data) {
                tweetList = data.results;
                parseTweets();
                updateHashLinks();
            },
            error: function (data) {
                console.log("error");
                console.log(data);

            }
        })
    }

    if (fetchOneID) {
        fetchSingle(fetchOneID)
    } else {
        fetchTweets()
    }

    $("#loadmore").click(function (event) {
        event.preventDefault();
        if (nextTweetURL) {
            fetchTweets(nextTweetURL);
        }
    });

    var charsStart = 140;
    var charsCurrent = 0;

    $("#tweet-form").append(`<span class="tweetCharsLeft" style="margin-left: 20px;">${charsStart}</span>`);

    $("#tweet-form textarea").bind('input propertychange', function (event) {
        var tweetValue = $(this).val();
        charsLeft = charsStart - tweetValue.length;
        var spanChars = $(".tweetCharsLeft");
        spanChars.text(charsLeft);
        if (charsLeft > 0) {
            spanChars.removeClass("grey-color");
            spanChars.removeClass("red-color");
        } else if (charsLeft == 0) {
            spanChars.removeClass("red-color");
            spanChars.addClass("grey-color");
        } else if (charsLeft < 0) {
            spanChars.removeClass("grey-color");
            spanChars.addClass("red-color");
        }
    });

    $("#tweet-form").submit(function (event) {
        event.preventDefault();
        var this_ = $(this);
        var formData = this_.serialize();
        if (charsCurrent >= 0) {
            $.ajax({
                url: "/api/tweet/create/",
                data: formData,
                method: "POST",
                success: function (data) {
                    this_.find("input[type=text], textarea").val("");
                    attachTweet(data, true);
                    updateHashLinks();
                    $("#replyModal").modal("hide");
                },
                error: function (data) {
                    console.log("error");
                    console.log(data);
                }
            })
        } else {
            console.log("Tweet is too long.")
        }
    });
}

