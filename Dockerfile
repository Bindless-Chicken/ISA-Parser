FROM ruby:2

RUN gem install jekyll bundler

EXPOSE 4000

CMD bundle exec jekyll serve --livereload