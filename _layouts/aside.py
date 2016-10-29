<aside>
    <nav class="chrono">
        {% if post.next.url %}
        <a class="go-left sakura-blossom no-border" href="{{post.next.url}}">&laquo; {{post.next.title}} </a>
        {% endif %}
        {% if post.previous.url %}
        <a class="go-right sakura-fade no-border" href="{{post.previous.url}}">{{post.previous.title}} &raquo;</a>
        {% endif %}
    </nav>
    <div style="clear: both;"></div>
</aside>
