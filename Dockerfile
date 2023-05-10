FROM nginx
ADD ./ /usr/share/nginx/html
CMD ["/usr/share/nginx/html/tuneindex.sh"]
EXPOSE 80