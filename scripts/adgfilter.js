const fs = require('fs').promises
const https = require('https')
const path = require('path')

// Local destination folder path
const destinationFolder = process.cwd()

// Generate AdGuard DNS filter for Surge
async function generateDnsFilter () {
  const url = 'https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_15_DnsFilter/filter.txt'

  const domainsToExclude = ['*', 'logs.netflix.com', 'example1.example.com', 'example2.example.com', 'example3.example.com']

  try {
    const data = await new Promise((resolve, reject) => {
      https
        .get(url, (res) => {
          let data = ''

          res.on('data', (chunk) => {
            data += chunk
          })

          res.on('end', () => resolve(data))
          res.on('error', reject)
        })
        .on('error', reject)
    })

    const lines = data.split('\n').map((line) => line.trim())

    const filteredLines = lines
      .filter((line) => {
        return line.startsWith('||') && line.endsWith('^') && !domainsToExclude.some((domain) => line.includes(domain))
      })
      .map((line) => {
        return '.' + line.replace(/^\|\|([^|^]+)\^$/, '$1')
      })

    if (filteredLines.length > 0) {
      // Get current timestamp in Eastern Standard Time (EST)
      const date = new Date()
      const estTime = date.toLocaleString('en-US', { timeZone: 'America/New_York' })

      // Write the filtered content to a file with timestamp comments
      await fs.writeFile(
        path.join(destinationFolder, 'dnsfilters.txt'),
        `# AdGuard DNS filter for Surge Generated from ${url}\n` +
          `# Updated at ${estTime} (EST)\n` +
          `# Total lines: ${filteredLines.length}\n` +
          '# https://github.com/rnlo/r\n' +
          `${filteredLines.join('\n')}\n`
      )
      console.log(`AdGuard DNS filter for Surge Generated from ${url} and saved to dnsfilters.txt.`) // Changed to console.log
    } else {
      console.log('Result has less than 1 lines. Not writing to file.') // Changed to console.log
    }
  } catch (error) {
    console.error(`Failed to download file due to error: ${error.message}`) // Changed to console.error
  }
}

generateDnsFilter()
