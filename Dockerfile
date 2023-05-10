FROM nginx
COPY tuneindex.sh /usr/share/nginx/tuneindex.sh
RUN chmod +x /usr/share/nginx/tuneindex.sh
CMD ["/usr/share/nginx/tuneindex.sh"]
ADD ./ /usr/share/nginx/html
EXPOSE 80