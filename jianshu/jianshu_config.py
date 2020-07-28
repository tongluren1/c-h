
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
    }
}
