
<h4>Add a new member to your group</h4>
<form method="POST" autocomplete="off">
    {% csrf_token %}

    {{form.as_p}}

    <input type="submit" value="Add member">
</form>
