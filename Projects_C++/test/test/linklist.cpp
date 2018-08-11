template<class T>
class slistNode
{
    public:
    slistNode(){next=NULL;}
    T data;//值
    slistNode* next;//指向下一个节点的指针
};
template<class T>
class myslist
{
    private:
    unsigned int listlength;
    slistNode<T>* node;//临时节点
	slistNode<T>* headnode;//头节点
    slistNode<T>* lastnode;//尾结点
    public:
        myslist();//初始化
        unsigned int length();//链表元素的个数
        void add(T x);//表尾添加元素
        void traversal();//遍历整个链表并打印
        bool isEmpty();//判断链表是否为空
        slistNode<T>* find(T x);//查找值为x的节点,返回节点的地址,找不到返回NULL
        void Delete(T x);//删除值为x的节点
        void insert(T x,slistNode<T>* p);//在p节点后插入值为x的节点
        void insertHead(T x);//在链表的头部插入节点

};
template<class T>
myslist<T>::myslist()
{
    node=NULL;
    lastnode=NULL;
    headnode=NULL;
    listlength=0;
}
template<class T>
inline unsigned int myslist<T>::length(){return listlength;}

template<class T>
void  myslist<T>::add(T x)
{
    node=new slistNode<T>();//申请一个新的节点
    node->data=x;//新节点赋值为x
    if(lastnode==NULL)//如果没有尾节点则链表为空,node既为头结点,又是尾节点
    {
        headnode=node;
        lastnode=node;
    }
    else//如果链表非空
    {
        lastnode->next=node;//node既为尾节点的下一个节点
        lastnode=node;//node变成了尾节点,把尾节点赋值为node
    }
    ++listlength;//元素个数+1
}

template<class T>
void  myslist<T>::traversal()
{
    node=headnode;//用临时节点指向头结点
    while(node!=NULL)//遍历链表并输出
    {
        cout<<node->data<<ends;
        node=node->next;
    }
    cout<<endl;
}
template<class T>
bool  myslist<T>::isEmpty()
{
    return listlength==0;
}
template<class T>
slistNode<T>* myslist<T>::find(T x)
{
    node=headnode;//用临时节点指向头结点
    while(node!=NULL&&node->data!=x)//遍历链表,遇到值相同的节点跳出
    {
        node=node->next;
    }
    return node;//返回找到的节点的地址,如果没有找到则返回NULL
}
template<class T>
void  myslist<T>::Delete(T x)
{
    slistNode<T>* temp=headnode;//申请一个临时节点指向头节点
    if(temp==NULL) return;//如果头节点为空,则该链表无元素,直接返回
    if(temp->data==x)//如果头节点的值为要删除的值,则删除投节点
    {
        headnode=temp->next;//把头节点指向头节点的下一个节点
        if(temp->next==NULL) lastnode=NULL;//如果链表中只有一个节点,删除之后就没有节点了,把尾节点置为空
        delete(temp);//删除头节点
        return;
    }
    while(temp->next!=NULL&&temp->next->data!=x)//遍历链表找到第一个值与x相等的节点,temp表示这个节点的上一个节点
    {
        temp=temp->next;
    }
    if(temp->next==NULL) return;//如果没有找到则返回
    if(temp->next==lastnode)//如果找到的时候尾节点
    {
        lastnode=temp;//把尾节点指向他的上一个节点
        delete(temp->next);//删除尾节点
        temp->next=NULL;
    }
    else//如果不是尾节点
    {
        node=temp->next;//用临时节点node指向要删除的节点
        temp->next=node->next;//要删除的节点的上一个节点指向要删除节点的下一个节点
        delete(node);//删除节点
        node=NULL;
    }
}
template<class T>
void  myslist<T>::insert(T x,slistNode<T>* p)
{
    if(p==NULL) return;
    node=new slistNode<T>();//申请一个新的空间
    node->data=x;
    node->next=p->next;
    p->next=node;
    if(node->next==NULL)//如果node为尾节点
    lastnode=node;
}
template<class T>
void  myslist<T>::insertHead(T x)
{
    node=new slistNode<T>();
    node->data=x;
    node->next=headnode;
    headnode=node;
}

template<class T>
void main()
{
	cout << "hello world----" << endl;
	myslist<T> *objMylist;
	objMylist->add("tail");
	objMylist->insertHead("head");
}