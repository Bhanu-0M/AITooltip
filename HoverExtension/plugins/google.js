var hoverZoomPlugins = hoverZoomPlugins || [];
hoverZoomPlugins.push({
    name:'Google',
    version:'4.3',
    prepareImgLinks:function (callback) {
        var res = [];

        function summarizeHoveredLink(linkElement, callback) {
            const linkUrl = linkElement.attr('href');
            if (!linkUrl || linkUrl.startsWith('javascript:')) {
                if (callback && typeof callback === 'function') callback(null);
                return;
            }

            fetch('http://localhost:5000/process_link', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ link: linkUrl })
            })
            .then(response => {
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                return response.text();
            })
            .then(responseText => {
                console.log('Received response text:', responseText);
                try {
                    const summaryJson = JSON.parse(responseText);
                    const summaryData = summaryJson.data;

                    if (summaryData && typeof summaryData === 'string' && summaryData.trim() !== "" && typeof hoverZoom !== 'undefined' && hoverZoom.util && hoverZoom.util.textToImageDataUrl) {
                        console.log('Extracted summary data for image:', summaryData);
                        const imageOptions = {
                            fontSize: (hoverZoom.options && hoverZoom.options.fontSize) ? hoverZoom.options.fontSize : 16,
                            maxWidth: (hoverZoom.options && hoverZoom.options.maxWidth && hoverZoom.options.maxWidth > 0) ? Math.min(600, hoverZoom.options.maxWidth - 40) : 600,
                        };
                        const imageDataUrl = hoverZoom.util.textToImageDataUrl(summaryData, imageOptions);
                        if (callback && typeof callback === 'function') callback(imageDataUrl);
                    } else {
                        console.warn('Summary data is missing, not a string, or empty.');
                        if (callback && typeof callback === 'function') callback(null);
                    }
                } catch (e) {
                    console.error('Error parsing summary JSON or processing data for ' + linkUrl + ':', e);
                    console.warn('Original responseText was:', responseText);
                    if (callback && typeof callback === 'function') callback(null);
                }
            })
            .catch(error => {
                console.error('Error fetching or processing summary for ' + linkUrl + ':', error);
                if (callback && typeof callback === 'function') callback(null);
            });
        }

        // Add hover event listener for all links in Google search results
        $('a[href^="http"], a[href^="https"], a[href^="/"]').not('#hzViewer a, #hzLoader a').each(function() {
            const link = $(this);
            
            if (link.closest('#hzViewer, #hzLoader').length > 0) {
                return;
            }

            link.off('mouseenter.summaryHover').on('mouseenter.summaryHover', function() {
                const $currentLink = $(this);

                const existingSrc = $currentLink.data().hoverZoomSrc;
                if ($currentLink.data('summaryFetching') || 
                    (existingSrc && existingSrc.length > 0 && existingSrc[0].startsWith('data:image/'))) {
                    return;
                }
                if (existingSrc && existingSrc.length > 0 && !existingSrc[0].startsWith('data:')) {
                    return;
                }

                $currentLink.data('summaryFetching', true);

                summarizeHoveredLink($currentLink, function(imageDataUrl) {
                    $currentLink.removeData('summaryFetching');
                    if (imageDataUrl) {
                        $currentLink.data().hoverZoomSrc = [imageDataUrl];
                        if (!$currentLink.hasClass('hoverZoomLink')) {
                            $currentLink.addClass('hoverZoomLink');
                        }
                        $currentLink.trigger('mousemove');
                    }
                });
            });
        });

        callback($(res), this.name);
    }
});
