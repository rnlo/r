const fs = require('fs').promises
const https = require('https')
const path = require('path')

const fileNamesDict = {
  'temp.list': [
    'temprule.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/ByteDance/ByteDance.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Zhihu/Zhihu.list'
  ],
  'domain.list': [
    'domainrule.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/GitHub/GitHub.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/OpenAI/OpenAI.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Copilot/Copilot.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Telegram/Telegram.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/YouTube/YouTube.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/TikTok/TikTok.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Spotify/Spotify.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Discord/Discord.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/PayPal/PayPal.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Twitter/Twitter.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Wikipedia/Wikipedia.list'
  ],
  'streaminggeo.list': [
    'streaminggeorule.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/HuluUSA/HuluUSA.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Sling/Sling.list'
  ],
  'streaming.list': [
    'streamingrule.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/AmazonPrimeVideo/AmazonPrimeVideo.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Peacock/Peacock.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Twitch/Twitch.list'
  ],
  'cn.list': [
    'cnrule.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Alibaba/Alibaba_All_No_Resolve.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Tencent/Tencent.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/WeChat/WeChat.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/ByteDance/ByteDance.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/NetEase/NetEase.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Baidu/Baidu.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/XiaoMi/XiaoMi.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/MeiTuan/MeiTuan.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Zhihu/Zhihu.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/JingDong/JingDong.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Youku/Youku.list',
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/CIBN/CIBN.list'
  ]
}

const destinationFolder = process.cwd()

async function getFileContent (fileName) {
  try {
    if (fileName.startsWith('http://') || fileName.startsWith('https://')) {
      return new Promise((resolve, reject) => {
        https
          .get(fileName, (resp) => {
            if (resp.statusCode !== 200) {
              console.log(`Error: Status code ${resp.statusCode}. URL: ${fileName}`)
              resolve(null)
              return
            }
            let data = ''
            resp.on('data', (chunk) => {
              data += chunk
            })
            resp.on('end', () => {
              resolve(data)
            })
          })
          .on('error', (err) => {
            console.log(`Error: ${err.message}. URL: ${fileName}`)
            resolve(null)
          })
      })
    } else {
      await fs.access(fileName)
      return fs.readFile(fileName, 'utf8')
    }
  } catch (err) {
    console.log(`Error: ${err.message}. File/URL: ${fileName}`)
    return null
  }
}

async function copyFilesToDestination (fileNamesDict) {
  for (const [destinationFileName, fileNames] of Object.entries(fileNamesDict)) {
    const destinationFilePath = path.join(destinationFolder, destinationFileName)
    let lines = []
    try {
      await fs.access(destinationFilePath)
      const content = await fs.readFile(destinationFilePath, 'utf8')
      lines = content.split('\n')
      const endLineIndex = lines.findIndex((line) => line.includes('# End rnlo rules'))
      if (endLineIndex !== -1) {
        lines = lines.slice(0, endLineIndex + 2)
      }
    } catch (err) {
      console.log(`Error: ${err.message}. File: ${destinationFilePath}`)
    }

    const results = await Promise.allSettled(fileNames.map(getFileContent))
    for (const [index, result] of results.entries()) {
      if (result.status === 'fulfilled' && result.value !== null) {
        lines.push(result.value)
        console.log(`File copied from ${fileNames[index]} and added to ${destinationFileName}.`)
      }
    }
    lines.push('')
    await fs.writeFile(destinationFilePath, lines.join('\n'))
  }
}

copyFilesToDestination(fileNamesDict).catch(console.error)
