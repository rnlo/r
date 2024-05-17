const fs = require('fs').promises
const https = require('https')
const path = require('path')

// Local destination folder path
const destinationFolder = process.cwd()

// Generate China IP filter for Surge
async function generateIpFilter () {
  try {
    const url = 'https://raw.githubusercontent.com/misakaio/chnroutes2/master/chnroutes.txt'

    const domainsToExclude = ['#', 'exampleip1', 'exampleip2', 'exampleip3']

    await new Promise((resolve, reject) => {
      https
        .get(url, (response) => {
          let data = ''
          response.on('data', (chunk) => {
            data += chunk
          })
          response.on('end', async () => {
            const lines = data.split('\n')

            const filteredLines = lines
              .filter((line) => line.trim() !== '' && !domainsToExclude.some((excludeItem) => line.includes(excludeItem)))
              .map((line) => 'IP-CIDR,' + line)

            if (filteredLines.length > 0) {
              const estTime = new Date().toLocaleString('en-US', { timeZone: 'America/New_York' })

              await fs.writeFile(
                path.join(destinationFolder, 'CNIP.list'),
                `# China IP for Surge Generated from ${url}\n` +
                  `# Updated at ${estTime} (EST)\n` +
                  `# Total lines: ${filteredLines.length}\n` +
                  '# https://github.com/rnlo/r\n' +
                  `${filteredLines.join('\n')}\n`
              )
              console.log(`China IP for Surge Generated from ${url} and saved to CNIP.list.`)
            } else {
              console.log('Result has less than 1 lines. Not writing to file.')
            }
            resolve()
          })
        })
        .on('error', (error) => {
          console.error(`An error occurred while fetching the file from '${url}': ${error}`)
          console.error(error.stack)
          reject(error)
        })
    })
  } catch (error) {
    console.error(`An error occurred: ${error}`)
    console.error(error.stack)
  }
}

generateIpFilter()
