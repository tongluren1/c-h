# -*- coding: utf-8

base_url = 'https://www.jianshu.com/'

pattern_model = {
    'article_list': {
        'box_pattern': '(<li id="note-\d+?" data-note-id="\d+?" class="[\s\S]*?">[\s\S]*?</li>)',
        'des_pattern': {
            'ArticleID': '<a class="title" target="_blank" href="/p/(\S+?)">',
            'NoteId': '<li id="note-\d+?" data-note-id="(\d+?)"',
            'Title': '<a class="title" target="_blank" href="/p/\S+?">([\s\S]*?)</a>',
            'Abstract': '<p class="abstract">\s*?([\s\S]*?)\s*?</p>',
            'Paid': '<i class="iconfont ic-paid1"></i>\s*?(\S+?)\s*?</span>',
            'ReadNum': '<i class="iconfont ic-list-read"></i>\s*?(\S+?)\s*?</a>',
            'CommentsNum': '<i class="iconfont ic-list-comments"></i>\s*?(\S+?)\s*?</a>',
            'LikeNum': '<span><i class="iconfont ic-list-like"></i>\s*?(\S+?)\s*?</span>',
            'CreateTime': '<span class="time" data-shared-at="(\S+?)T(\S+?)\+08:00">'
        }
    },
    'article_info': {
        'box_pattern': '(\{"dataManager":[\s\S]*?"\})</script>'
    },
    'user_list': {
        'box_pattern': '(<div class="col-xs-8">[\s\S]*?</div>\s*?</div>\s*?</div>)',
        'des_pattern': {
            'UserId': '<a target="_blank" href="/users/(\S+?)">',
            'NickName': '<h4 class="name">\s*?(\S*?)\s*?(?:</h4>|<i)',
            'Sex': '<i class="iconfont ic-(\S+?)"></i>\s*?</h4>',
            'HomeUrl': '<a target="_blank" href="(\S+?)">',
            'Avatar': '<img class="avatar" src="(\S+?)"',
            'Aaying': '<p class="description">\s*?([\s\S]*?)\s*?</p>',
            'RecentUpdate': '<a class="new" target="_blank" href="(\S+?)">(\S+?)</a>',
        }
    },
    'user_list_info': {
        'box_pattern': '(<div class="info">\s*?<ul>\s*?[\s\S]*?\s*?</ul>\s*?</div>\s*?</div>)',
        'intro_pattern': '<div class="js-intro">([\s\S]*?)</div>',
        'des_pattern': '<p>(\S+?)</p>'
    },
    'like_user_list': {
        'box_pattern': '(<li>\s*?<a class="avatar"[\s\S]*?</li>)',
        'des_pattern': {
            'UserId': '<a class="avatar" href="/u/(\S*?)">',
            'NickName': '<a class="name" href="/u/\S*?">(\S*?)</a>',
            'Sex': '<i class="iconfont ic-(\S+?)"></i>',
            'HomeUrl': '<a class="avatar" href="(\S*?)">',
            'Avatar': '<img src="([\s\S]*?)"[\s\S]*?/>',
        }
    },
}
