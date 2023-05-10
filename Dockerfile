FROM nginx
CMD ["/usr/share/nginx/html/tuneindex.sh"]
ADD ./ /usr/share/nginx/html
EXPOSE 80