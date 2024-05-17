const fs = require('fs').promises
const https = require('https')
const path = require('path')

const filterParameters = {
  sourceFiles: {
    'https://raw.githubusercontent.com/LM-Firefly/Rules/master/PROXY/Amazon.list': 'Amazon.list'
    // "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Amazon/Amazon.list": "AmazonAll.list",
    // "https://raw.githubusercontent.com/LM-Firefly/Rules/master/PROXY/Google.list": "GoogleAll.list"
  },
  markers: {
    '## >> Amazon Prime Video': '## >> Audible'
    // "## >> CreateSpace": "## >> End CreateSpace",
    // "## >> Youtube": "## >> End Youtube"
  },
  linesToExclude: [
    'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/AmazonPrimeVideo/AmazonPrimeVideo.list',
    'example1.example.com',
    'example2.example.com'
  ]
}

const destinationFolder = process.cwd()

function httpsGet (url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = ''

      res.on('data', (chunk) => {
        data += chunk
      })

      res.on('end', () => resolve(data))
      res.on('error', reject)
    })
  })
}

async function fetchAndFilterContent (filterParameters) {
  let linesToExclude = await Promise.all(
    filterParameters.linesToExclude.map(async (line) => {
      if (line.startsWith('http://') || line.startsWith('https://')) {
        try {
          const data = await httpsGet(line)
          return data.split('\n').filter((line) => !line.startsWith('#'))
        } catch (error) {
          console.error(`Failed to fetch data from ${line}: ${error}`)
          return []
        }
      } else {
        return [line]
      }
    })
  )
  linesToExclude = linesToExclude.flat()

  const [sourceUrl, filteredFile] = Object.entries(filterParameters.sourceFiles)[0]
  try {
    let data = await httpsGet(sourceUrl)
    Object.entries(filterParameters.markers).forEach(([begin, end]) => {
      const pattern = new RegExp(`${escapeRegExp(begin)}.*?(?=${escapeRegExp(end)})`, 'gs')
      data = data.replace(pattern, '')
    })

    linesToExclude.forEach((lineToExclude) => {
      data = data.replace(lineToExclude, '')
    })

    await fs.writeFile(path.join(destinationFolder, filteredFile), data)
    console.log(`File copied from ${sourceUrl} filtered and added to ${filteredFile}.`)
  } catch (error) {
    console.error(`Failed to process file ${sourceUrl}: ${error}`)
  }
}

function escapeRegExp (string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

fetchAndFilterContent(filterParameters)
