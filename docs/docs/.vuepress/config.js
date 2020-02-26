module.exports = {
    title: 'H1ve',
    description: 'D0g3 @ 道格安全研究实验室',
    themeConfig: {
      // logo: '/assets/img/logo.png',
      nav: [
          { text: '指南', link: '/guide/' },
          {
              text: '插件',
              items: [
                { text: 'CTFd-Owl', link: '/guide/ctfd-owl'},
                { text: 'CTFd-Glowworm', link: '/guide/ctfd-glowworm'}
              ]
            }
        ],
      sidebar: [
          {
              title: '指南',
            //   path: '/guide/',
              collapsable: false, // 可选的, 默认值是 true,
              sidebarDepth: 2,    // 可选的, 默认值是 1
              children: [
                '/guide/run',
                '/guide/troubles'
              ]
          },
          {
              title: '插件',
              collapsable: false, // 可选的, 默认值是 true,
              sidebarDepth: 2,    // 可选的, 默认值是 1
              children: [
                '/guide/ctfd-owl',
                '/guide/ctfd-glowworm'
              ]
          }
      ],
      lastUpdated: 'Last Updated',
      displayAllHeaders: true,
      sidebarDepth: 2,
      smoothScroll: true,
      // 假定是 GitHub. 同时也可以是一个完整的 GitLab URL
      repo: 'https://github.com/D0g3-Lab/H1ve',
      // 自定义仓库链接文字。默认从 `themeConfig.repo` 中自动推断为
      // "GitHub"/"GitLab"/"Bitbucket" 其中之一，或是 "Source"。
      repoLabel: 'GitHub',
      docsDir: 'docs/docs',
      // 假如文档放在一个特定的分支下：
      docsBranch: 'dev',
      // 默认是 false, 设置为 true 来启用
      editLinks: true,
      // 默认为 "Edit this page"
      editLinkText: '在 GitHub 上编辑此页'
    },
    markdown: {
        lineNumbers: true
    }
  }
  