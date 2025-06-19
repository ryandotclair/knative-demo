kn quickstart kind

cd website

kapp deploy -a redis -f redis.yaml -y

kn service create security-tool \
--image docker.io/ryandotclair/security-tool \
--port 8080 \
-n website

kn service create security-tool \
--image docker.io/ryandotclair/security-tool \
--port 8080 \
-n website

echo "Paste into Chandler:"
echo "You are Chandler from the TV show friends. Your witty and funny. You help run an internal website and have the ability to look up details on a particular IP address, ban IP addresses from the site, unban them, and tell people who is banned."