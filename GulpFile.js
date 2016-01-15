var gulp = require('gulp');
var gutil = require('gulp-util');
var sass = require('gulp-sass');
var coffee = require('gulp-coffee');
var concat = require('gulp-concat');
var cssnano = require('gulp-cssnano');

gulp.task('styles', function() {
    return gulp.src('./morningglory/blog/sass/**/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('./morningglory/blog/css/'))
});

gulp.task('style-copy', ['styles'], function() {
    return gulp.src('./morningglory/blog/css/*style.css')
        .pipe(gulp.dest('./morningglory/blog/static/blog/'));
});

gulp.task('minify-css', ['style-copy'], function() {
    return gulp.src('./morningglory/blog/static/blog/*.css')
        .pipe(cssnano())
        .pipe(gulp.dest('./morningglory/blog/static/blog/'));
});

gulp.task('all', ['style-copy']);
gulp.task('deploy' ['minify-css']);