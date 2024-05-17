const fs = require('fs')
const https = require('https')
const path = require('path')

// Dictionary of file URLs and new file names
const fileUrls = {
  'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Apple/Apple_All_No_Resolve.list': 'Apple.list',
  'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Microsoft/Microsoft.list': 'Microsoft.list',
  'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Google/Google.list': 'Google.list',
  'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Facebook/Facebook.list': 'Facebook.list',
  'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/AmazonIP/AmazonIP.list': 'AmazonIP.list',
  'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Netflix/Netflix.list': 'Netflix.list',
  'https://iptv-org.github.io/iptv/countries/us.m3u': 'us.m3u'
}

// Local destination folder path
const destinationFolder = process.cwd()

// Download list files from file_urls
function downloadFile (fileUrl, newFileName) {
  return new Promise((resolve, reject) => {
    const targetFile = path.join(destinationFolder, newFileName)
    const file = fs.createWriteStream(targetFile)

    https
      .get(fileUrl, function (response) {
        response.pipe(file)
        file.on('finish', function () {
          file.close()
          console.log(`File copied from ${fileUrl} and saved to ${newFileName}.`)
          resolve()
        })
      })
      .on('error', function (err) {
        fs.unlink(targetFile)
        console.error(`Error occurred while downloading ${fileUrl}. Error: ${err.message}`)
        reject(err)
      })
  })
}

async function downloadFilesInParallel (fileUrls) {
  const promises = []
  for (const [fileUrl, newFileName] of Object.entries(fileUrls)) {
    promises.push(downloadFile(fileUrl, newFileName))
  }
  const results = await Promise.allSettled(promises)

  for (const result of results) {
    if (result.status === 'rejected') {
      console.error(`Error occurred while downloading a file. Error: ${result.reason}`)
    }
  }
}

downloadFilesInParallel(fileUrls)
  .then(() => console.log('All files downloaded successfully'))
  .catch((err) => console.error(`Error occurred while downloading files. Error: ${err.message}`))
