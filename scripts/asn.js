const fs = require('fs').promises
const https = require('https')
const path = require('path')

// Local destination folder path
const destinationFolder = process.cwd()

const regionAndFlag = {
  CN: '🇨🇳', // China
  US: '🇺🇸' // United States
}

const options = {
  headers: {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15'
  }
}

async function getAndParseData (regionCode) {
  const url = `https://bgp.he.net/country/${regionCode}`
  return new Promise((resolve, reject) => {
    try {
      https
        .get(url, options, (res) => {
          let data = ''

          res.on('data', (chunk) => {
            data += chunk
          })

          res.on('end', () => {
            const regex = /<tr>\s*<td><a href="\/(AS\d+)"[^>]*>(.*?)<\/a><\/td>\s*<td[^>]*>.*?<\/td>\s*<td class='alignright'>(.*?)<\/td>/g
            let match
            const selectedData = []

            while ((match = regex.exec(data)) !== null) {
              if (match[3] !== '0') {
                const asn = match[1].replace('AS', 'IP-ASN,')
                selectedData.push(asn)
              }
            }

            resolve({ selectedData, url })
          })
        })
        .on('error', (error) => {
          console.log(`Error occurred while scraping data for region code ${regionCode}. Error: ${error}`)
          reject(error)
        })
    } catch (error) {
      console.log(`Error occurred while sending request for region code ${regionCode}. Error: ${error}`)
      reject(error)
    }
  })
}

async function writeDataToFile (regionCode, selectedData, url) {
  if (selectedData.length > 0) {
    const estTime = new Date().toLocaleString('en-US', { timeZone: 'America/New_York' })
    const regionFlag = regionAndFlag[regionCode.toUpperCase()] || ''

    try {
      await fs.writeFile(
        path.join(destinationFolder, `ASN${regionCode}.list`),
        `# ${regionFlag}${regionCode}ASN Generated from ${url}\n` +
          `# Updated at ${estTime} (EST)\n` +
          `# Total lines: ${selectedData.length}\n` +
          '# https://github.com/rnlo/r\n' +
          `${selectedData.join('\n')}\n`
      )
      console.log(`${regionCode}ASN Generated from ${url} and saved to ASN${regionCode}.list.`)

      const sortedData = selectedData.sort()
      await fs.writeFile(path.join(destinationFolder, `A${regionCode}.list`), `${sortedData.join('\n')}\n`)
      console.log(`${regionCode}ASN Generated from ${url} sorted and saved to A${regionCode}.list.`)
    } catch (error) {
      console.log(`Error occurred while writing data to file for region code ${regionCode}. Error: ${error}`)
    }
  } else {
    console.log(`Result has less than 1 lines for ${regionCode}. Not writing to file.`)
  }
}

async function scrapeData () {
  for (const regionCode of Object.keys(regionAndFlag)) {
    try {
      const { selectedData, url } = await getAndParseData(regionCode)

      if (!selectedData || !url) {
        console.log(`Skipping region code ${regionCode} due to missing data.`)
        continue
      }

      writeDataToFile(regionCode, selectedData, url)

      // Add a random delay between requests
      await new Promise((resolve) => setTimeout(resolve, Math.random() * (3000 - 1000) + 1000))
    } catch (error) {
      console.log(`Error occurred while scraping data for region code ${regionCode}. Error: ${error}`)
    }
  }
}

scrapeData()
