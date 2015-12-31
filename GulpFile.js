var gulp = require('gulp');
var gutil = require('gulp-util');
var sass = require('gulp-sass');
var coffee = require('gulp-coffee');
var concat = require('gulp-concat');

gulp.task('styles', function() {
    return gulp.src('./morningglory/blog/sass/**/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('./morningglory/blog/css/'))
});

gulp.task('style-copy', ['styles'], function() {
    gulp.src('./morningglory/blog/css/style.css')
        .pipe(gulp.dest('./morningglory/blog/static/blog/'));
});

gulp.task('all', ['style-copy']);