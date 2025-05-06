cmake_minimum_required(VERSION 3.10)

# Discover all HTML fragment files
file(GLOB HTML_FRAGMENTS "${CMAKE_CURRENT_SOURCE_DIR}/fragments/*.html")

# Get the example CV path
set(EXAMPLE_CV "${CMAKE_CURRENT_SOURCE_DIR}/../example/cv.md")

# Test with example CV
add_test(
  NAME test_html_rendering_example_cv
  COMMAND python3 ${CMAKE_CURRENT_SOURCE_DIR}/test_html_rendering.py --cv ${EXAMPLE_CV}
)

# Test with the default test CV (built into script)
add_test(
  NAME test_html_rendering_default_cv
  COMMAND python3 ${CMAKE_CURRENT_SOURCE_DIR}/test_html_rendering.py
)

# Make the test script executable
file(CHMOD ${CMAKE_CURRENT_SOURCE_DIR}/test_html_rendering.py 
     PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE)