\# Temp <https://cdn.jsdelivr.net/gh/rnlo/r@m/temp.list>  
RULE-SET,<https://raw.githubusercontent.com/rnlo/r/m/temp.list>,🌐 Proxy  
\# REJECT  
DOMAIN-SET,<https://raw.githubusercontent.com/rnlo/r/m/dnsfilters.txt>,REJECT  
\# Clients  
RULE-SET,<https://raw.githubusercontent.com/rnlo/r/m/Clients.list>,🌐 Proxy  
\# Domains  
RULE-SET,<https://raw.githubusercontent.com/rnlo/r/m/Apple.list>,🌐 Proxy  
RULE-SET,<https://raw.githubusercontent.com/rnlo/r/m/Microsoft.list>,🌐 Proxy  
RULE-SET,<https://raw.githubusercontent.com/rnlo/r/m/Google.list>,🌐 Proxy  
RULE-SET,<https://raw.githubusercontent.com/rnlo/r/m/Facebook.list>,🌐 Proxy  
RULE-SET,<https://raw.githubusercontent.com/rnlo/r/m/Amazon.list>,🌐 Proxy  
RULE-SET,<https://raw.githubusercontent.com/rnlo/r/m/domain.list>,🌐 Proxy  
\# Streaming  
RULE-SET,<https://raw.githubusercontent.com/rnlo/r/m/Netflix.list>,🍿 Netflix  
RULE-SET,<https://raw.githubusercontent.com/rnlo/r/m/streaminggeo.list>,📺 USTV  
RULE-SET,<https://raw.githubusercontent.com/rnlo/r/m/streaming.list>,📺 IPTV  
\# CN  
RULE-SET,<https://raw.githubusercontent.com/rnlo/r/m/cn.list>,DIRECT  
\# SYSTEM DIRECT GEOIP FINAL  
RULE-SET,SYSTEM,🌐 Proxy  
RULE-SET,LAN,DIRECT  
\# RULE-SET,<https://raw.githubusercontent.com/rnlo/r/m/CNIP.list>,DIRECT  
RULE-SET,<https://raw.githubusercontent.com/rnlo/r/m/ASNCN.list>,DIRECT  
FINAL,🌐 Proxy,dns-failed  
