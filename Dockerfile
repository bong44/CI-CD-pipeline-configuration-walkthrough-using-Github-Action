FROM nginx
ADD ./ /usr/share/nginx/html
RUN chmod +x /usr/share/nginx/html/tuneindex.sh
CMD ["/usr/share/nginx/html/tuneindex.sh"]
EXPOSE 80